# Copyright (C) @YO_UR_OFFICIAL_CRUSH
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode, ChatType
import hashlib
import random
import asyncio
from sunlomusic.db import db
from sunlomusic.core.logging import logger

def get_percentage(name1, name2):
    sorted_names = "".join(sorted([name1.lower().strip(), name2.lower().strip()]))
    hash_val = int(hashlib.md5(sorted_names.encode()).hexdigest(), 16)
    return (hash_val % 101)

def get_ship_message(percent, name1, name2):
    bar_length = 10
    filled = int((percent / 100) * bar_length)
    bar = "❤️" * filled + "🤍" * (bar_length - filled)
    
    if percent < 20:
        status = "💔 <b>Just Friends</b>"
    elif percent < 50:
        status = "🤝 <b>Good Friends</b>"
    elif percent < 80:
        status = "💖 <b>Great Match!</b>"
    elif percent < 100:
        status = "💘 <b>Made for Each Other</b>"
    else:
        status = "💞 <b>Perfect Soulmates (100%)</b>"

    return f"<b>❤️ Love Calculator ❤️</b>\n\n👤 <b>{name1}</b>\n➕\n👤 <b>{name2}</b>\n\n{bar} <b>{percent}%</b>\n\n<blockquote>{status}</blockquote>"

def register_fun_handlers(app: Client):
    @app.on_message(filters.command("love"))
    async def love_command(client, message: Message):
        args = message.text.split(maxsplit=1)
        name1, name2 = None, None

        if message.reply_to_message and message.reply_to_message.from_user:
            name1 = message.from_user.first_name
            name2 = message.reply_to_message.from_user.first_name
        elif len(args) > 1:
            names = args[1].split()
            if len(names) >= 2:
                name1 = names[0]
                name2 = names[1]
            else:
                await message.reply_text("**Usage:**\n`/love Name1 Name2`\nYa kisi ke message par reply karke `/love` likhein.")
                return
        else:
            await message.reply_text("**Usage:**\n`/love Name1 Name2`\nYa kisi ke message par reply karke `/love` likhein.")
            return

        percent = get_percentage(name1, name2)
        result_text = get_ship_message(percent, name1, name2)
        await message.reply_text(result_text, parse_mode=ParseMode.HTML)

    @app.on_message(filters.command("couple"))
    async def couple_toggle(client, message: Message):
        if message.chat.type == ChatType.PRIVATE:
            await message.reply_text("**Yeh command sirf groups mein kaam karti hai.**")
            return
            
        # Simple Admin Check
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status not in ["administrator", "creator", "owner"]:
                await message.reply_text("❌ **Sirf group admins hi yeh command use kar sakte hain.**")
                return
        except Exception:
            pass # Agar check fail ho toh command chalne dein
            
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.reply_text("**Usage:**\n`/couple on` - Auto Award ON\n`/couple off` - Auto Award OFF")
            return
            
        action = args[1].lower()
        if action == "on":
            await db.update_chat_settings(message.chat.id, {'couple_award': True})
            await message.reply_text("✅ **Auto Daily Couple Award ON ho gaya hai!**\nBot ab din mein 5 baar random jodi ko award dega.")
        elif action == "off":
            await db.update_chat_settings(message.chat.id, {'couple_award': False})
            await message.reply_text("❌ **Auto Daily Couple Award OFF kar diya gaya hai.**")
        else:
            await message.reply_text("**Invalid action. Use `/couple on` ya `/couple off`.**")

async def daily_couple_award_task(app: Client):
    await asyncio.sleep(60)
    while True:
        try:
            groups = await db.get_all_broadcast_groups()
            if groups:
                for group in groups:
                    chat_id = group.get('chat_id')
                    if not chat_id: continue
                    try:
                        settings = await db.get_chat_settings(chat_id)
                        if not settings.get('couple_award', True):
                            continue
                            
                        members = []
                        async for m in app.get_chat_members(chat_id, limit=50):
                            if not m.user.is_bot and not m.user.is_deleted:
                                members.append(m.user)
                        
                        if len(members) >= 2:
                            random.shuffle(members)
                            user1 = members[0]
                            user2 = members[1]
                            
                            percent = get_percentage(user1.first_name, user2.first_name)
                            mention1 = f"[{user1.first_name}](tg://user?id={user1.id})"
                            mention2 = f"[{user2.first_name}](tg://user?id={user2.id})"
                            
                            bar_length = 10
                            filled = int((percent / 100) * bar_length)
                            bar = "❤️" * filled + "🤍" * (bar_length - filled)
                            
                            text = (
                                f"👑 <b>DAILY BEST COUPLE AWARD</b> 👑\n\n"
                                f"🏆 Aaj ke sabse pyare jodi:\n\n"
                                f"{mention1} ❤️ {mention2}\n\n"
                                f"{bar} <b>{percent}%</b>\n\n"
                                f"<blockquote>✨ <i>Congratulations! Aap dono ko aaj ka Best Couple Award milta hai.</blockquote>"
                            )
                            
                            await app.send_message(chat_id, text, parse_mode=ParseMode.HTML)
                            await asyncio.sleep(5)
                    except Exception as e:
                        logger.error(f"Couple award error in {chat_id}: {e}")
                        continue
        except Exception as e:
            logger.error(f"Error in daily_couple_award_task: {e}")
        await asyncio.sleep(4 * 60 * 60)

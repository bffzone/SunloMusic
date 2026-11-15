import asyncio
import random
from sunlomusic.db import db
from sunlomusic.core.logging import logger
# Copyright (C) @YO_UR_OFFICIAL_CRUSH
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
import hashlib
import random

def get_percentage(name1, name2):
    # Deterministic hash so same names give same result
    sorted_names = "".join(sorted([name1.lower().strip(), name2.lower().strip()]))
    hash_val = int(hashlib.md5(sorted_names.encode()).hexdigest(), 16)
    return (hash_val % 101) # 0 to 100

def get_ship_message(percent, name1, name2):
    bar_length = 10
    filled = int((percent / 100) * bar_length)
    bar = "❤️" * filled + "🤍" * (bar_length - filled)
    
    if percent < 20:
        status = "💔 <b>Just Friends / Enemies</b>"
        quote = "Koi baat nahi, dosti mein sab jaayaz hai!"
    elif percent < 50:
        status = "🤝 <b>Good Friends</b>"
        quote = "Achi dosti ban sakti hai inki."
    elif percent < 80:
        status = "💖 <b>Great Match!</b>"
        quote = "Inme kaafi chemistry hai. Ek baar try karna banta hai!"
    elif percent < 100:
        status = "💘 <b>Made for Each Other</b>"
        quote = "Yeh toh ekdum perfect jodi hai. Shaadi pakki!"
    else:
        status = "💞 <b>Perfect Soulmates (100%)</b>"
        quote = "Dil toh ek hai, bas dhadkan alag hai. True Love!"

    return (
        f"<b>❤️ Love Calculator ❤️</b>\n\n"
        f"👤 <b>{name1}</b>\n"
        f"➕\n"
        f"👤 <b>{name2}</b>\n\n"
        f"{bar} <b>{percent}%</b>\n\n"
        f"<blockquote>{status}\n<i>{quote}</i></blockquote>"
    )

def register_fun_handlers(app: Client):
    @app.on_message(filters.command("love"))
    async def love_command(client, message: Message):
        args = message.text.split(maxsplit=1)
        name1, name2 = None, None

        if message.reply_to_message and message.reply_to_message.from_user:
            # User replied to someone
            name1 = message.from_user.first_name
            name2 = message.reply_to_message.from_user.first_name
        elif len(args) > 1:
            # User typed /love Name1 Name2
            names = args[1].split()
            if len(names) >= 2:
                name1 = names[0]
                name2 = names[1]
            else:
                await message.reply_text("**Usage:**\n`/love Name1 Name2`\nYa kisi ke message par reply karke `/ship` likhein.")
                return
        else:
            await message.reply_text("**Usage:**\n`/love Name1 Name2`\nYa kisi ke message par reply karke `/ship` likhein.")
            return

        percent = get_percentage(name1, name2)
        result_text = get_ship_message(percent, name1, name2)

        await message.reply_text(result_text, parse_mode=ParseMode.HTML)


async def daily_couple_award_task(app: Client):
    # Wait a bit before starting the loop to let bot fully start
    await asyncio.sleep(60)
    
    while True:
        try:
            groups = await db.get_all_broadcast_groups()
            if groups:
                for group in groups:
                    chat_id = group.get('chat_id')
                    if not chat_id: continue
                    
                    try:
                        members = []
                        # Fetch up to 50 members to prevent flood limits
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
                                f"<blockquote>✨ <i>Congratulations! Aap dono ko aaj ka Best Couple Award milta hai.</i></blockquote>"
                            )
                            
                            await app.send_message(chat_id, text, parse_mode=ParseMode.HTML)
                            await asyncio.sleep(2) # Delay to prevent flood wait
                            
                    except Exception as e:
                        logger.error(f"Failed to get members/send couple award in {chat_id}: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Error in daily_couple_award_task: {e}")
            
        # Sleep for 4 hours (roughly 5-6 times a day)
        await asyncio.sleep(4 * 60 * 60)

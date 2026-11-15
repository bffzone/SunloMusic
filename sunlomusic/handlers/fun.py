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
        f"<b>💘 Love Calculator 💘</b>\n\n"
        f"👤 <b>{name1}</b>\n"
        f"➕\n"
        f"👤 <b>{name2}</b>\n\n"
        f"{bar} <b>{percent}%</b>\n\n"
        f"<blockquote>{status}\n<i>{quote}</i></blockquote>"
    )

def register_fun_handlers(app: Client):
    @app.on_message(filters.command("ship"))
    async def ship_command(client, message: Message):
        args = message.text.split(maxsplit=1)
        name1, name2 = None, None

        if message.reply_to_message and message.reply_to_message.from_user:
            # User replied to someone
            name1 = message.from_user.first_name
            name2 = message.reply_to_message.from_user.first_name
        elif len(args) > 1:
            # User typed /ship Name1 Name2
            names = args[1].split()
            if len(names) >= 2:
                name1 = names[0]
                name2 = names[1]
            else:
                await message.reply_text("**Usage:**\n`/ship Name1 Name2`\nYa kisi ke message par reply karke `/ship` likhein.")
                return
        else:
            await message.reply_text("**Usage:**\n`/ship Name1 Name2`\nYa kisi ke message par reply karke `/ship` likhein.")
            return

        percent = get_percentage(name1, name2)
        result_text = get_ship_message(percent, name1, name2)

        await message.reply_text(result_text, parse_mode=ParseMode.HTML)

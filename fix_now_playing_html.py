import os
import re

msg_file = "sunlomusic/ui/messages.py"
if os.path.exists(msg_file):
    with open(msg_file, "r", encoding="utf-8") as f:
        code = f.read()

    # Naya Now Playing function (100% HTML)
    new_now_playing = '''    @staticmethod
    def now_playing(track: Dict, requested_by: str = "Unknown", current_time: int = 0, queue: List[Dict] = None, playlist_unfetched: int = 0) -> str:
        title = track.get('title', 'Unknown')
        message = "<emoji id='5334665104677941170'>🎵</emoji> <b>Music Playlist:</b>\\n\\n"

        req_id = track.get('requested_by_id')
        if req_id:
            req_mention = f'<a href="tg://user?id={req_id}">{requested_by}</a>'
        else:
            req_mention = requested_by

        message += f"<b>1. <emoji id='5222472119295684375'>🎸</emoji> {title}</b>\\n"
        message += f"<emoji id='5944970130554359187'>🏆</emoji> <b>Requested by:</b> {req_mention}\\n\\n"

        if queue and len(queue) > 1:
            for i, next_track in enumerate(queue[1:4], start=2):
                next_title = next_track.get('title', 'Unknown')
                if len(next_title) > 50:
                    next_title = next_title[:47] + "..."
                next_name = next_track.get('requested_by', 'Unknown')
                next_id = next_track.get('requested_by_id')
                if next_id:
                    next_mention = f'<a href="tg://user?id={next_id}">{next_name}</a>'
                else:
                    next_mention = next_name
                message += f"<b>{i}. <emoji id='5222472119295684375'>🎸</emoji> {next_title}</b>\\n"
                message += f"<emoji id='5944970130554359187'>🏆</emoji> <b>Requested by:</b> {next_mention}\\n\\n"

            shown = min(len(queue), 4)
            remaining_in_queue = len(queue) - shown
            total_remaining = remaining_in_queue + playlist_unfetched
            if total_remaining > 0:
                message += f"<b>✨ {total_remaining} tracks still in the playlist.....</b>"

        return message'''

    # Replace the old function
    pattern = r"    @staticmethod\n    def now_playing\(.*?return message"
    if re.search(pattern, code, flags=re.DOTALL):
        code = re.sub(pattern, new_now_playing, code, flags=re.DOTALL)
        with open(msg_file, "w", encoding="utf-8") as f:
            f.write(code)
        print("✅ messages.py mein now_playing fix ho gaya (HTML)!")
    else:
        print("❌ now_playing function nahi mila.")
cat << 'EOF' > complete_html_fix.py
import os
import re

# 1. Fix messages.py (Now Playing function)
msg_file = "sunlomusic/ui/messages.py"
if os.path.exists(msg_file):
    with open(msg_file, "r", encoding="utf-8") as f:
        code = f.read()

    new_now_playing = """    @staticmethod
    def now_playing(track: Dict, requested_by: str = "Unknown", current_time: int = 0, queue: List[Dict] = None, playlist_unfetched: int = 0) -> str:
        title = track.get('title', 'Unknown')
        message = "<emoji id='5334665104677941170'>🎵</emoji> <b>Music Playlist:</b>\\n\\n"

        req_id = track.get('requested_by_id')
        if req_id:
            req_mention = f'<a href="tg://user?id={req_id}">{requested_by}</a>'
        else:
            req_mention = requested_by

        message += f"<b>1. <emoji id='5222472119295684375'>🎸</emoji> {title}</b>\\n"
        message += f"<emoji id='5944970130554359187'>🏆</emoji> <b>Requested by:</b> {req_mention}\\n\\n"

        if queue and len(queue) > 1:
            for i, next_track in enumerate(queue[1:4], start=2):
                next_title = next_track.get('title', 'Unknown')
                if len(next_title) > 50:
                    next_title = next_title[:47] + "..."
                next_name = next_track.get('requested_by', 'Unknown')
                next_id = next_track.get('requested_by_id')
                if next_id:
                    next_mention = f'<a href="tg://user?id={next_id}">{next_name}</a>'
                else:
                    next_mention = next_name
                message += f"<b>{i}. <emoji id='5222472119295684375'>🎸</emoji> {next_title}</b>\\n"
                message += f"<emoji id='5944970130554359187'>🏆</emoji> <b>Requested by:</b> {next_mention}\\n\\n"

            shown = min(len(queue), 4)
            remaining_in_queue = len(queue) - shown
            total_remaining = remaining_in_queue + playlist_unfetched
            if total_remaining > 0:
                message += f"<b>✨ {total_remaining} tracks still in the playlist.....</b>"

        return message"""

    pattern = r"    @staticmethod\n    def now_playing\(.*?return message"
    if re.search(pattern, code, flags=re.DOTALL):
        code = re.sub(pattern, new_now_playing, code, flags=re.DOTALL)
        with open(msg_file, "w", encoding="utf-8") as f:
            f.write(code)
        print("✅ messages.py mein now_playing function fix ho gaya (HTML)!")

# 2. Fix services/player.py (Force HTML parsing on photo)
player_file = "sunlomusic/services/player.py"
if os.path.exists(player_file):
    with open(player_file, "r", encoding="utf-8") as f:
        code = f.read()

    # Add ParseMode.HTML to send_photo for the Now Playing card
    old_send = """new_msg = await bot_client.send_photo(
                                chat_id=chat_id,
                                photo=_temp_thumb,
                                caption=new_text,
                                reply_markup=new_markup
                            )"""
    new_send = """new_msg = await bot_client.send_photo(
                                chat_id=chat_id,
                                photo=_temp_thumb,
                                caption=new_text,
                                reply_markup=new_markup,
                                parse_mode=ParseMode.HTML
                            )"""
    
    if old_send in code:
        code = code.replace(old_send, new_send)
        print("✅ services/player.py mein send_photo par ParseMode.HTML laga diya!")
    else:
        # Fallback: just inject parse_mode where send_photo is used
        code = re.sub(r"(send_photo\([^)]*reply_markup=[^)]*)\)", r"\1, parse_mode=ParseMode.HTML)", code)

    # Ensure ParseMode is imported
    if "from pyrogram.enums import ParseMode" not in code:
        code = "from pyrogram.enums import ParseMode\n" + code

    with open(player_file, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ services/player.py updated.")

print("🎉 Process Complete! Ab check karein.")

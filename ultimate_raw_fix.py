import os
import re

msg_file = "sunlomusic/ui/messages.py"
if os.path.exists(msg_file):
    with open(msg_file, "r", encoding="utf-8") as f:
        code = f.read()

    # Notice the r before the triple quotes (Raw String)
    new_func = r'''    @staticmethod
    def now_playing(track: Dict, requested_by: str = "Unknown", current_time: int = 0, queue: List[Dict] = None, playlist_unfetched: int = 0) -> str:
        title = track.get('title', 'Unknown')
        message = "<emoji id='5334665104677941170'>🎵</emoji> <b>Music Playlist:</b>\n\n"

        req_id = track.get('requested_by_id')
        if req_id:
            req_mention = f'<a href="tg://user?id={req_id}">{requested_by}</a>'
        else:
            req_mention = requested_by

        message += f"<b>1. <emoji id='5222472119295684375'>🎸</emoji> {title}</b>\n"
        message += f"<emoji id='5944970130554359187'>🏆</emoji> <b>Requested by:</b> {req_mention}\n\n"

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
                message += f"<b>{i}. <emoji id='5222472119295684375'>🎸</emoji> {next_title}</b>\n"
                message += f"<emoji id='5944970130554359187'>🏆</emoji> <b>Requested by:</b> {next_mention}\n\n"

            shown = min(len(queue), 4)
            remaining_in_queue = len(queue) - shown
            total_remaining = remaining_in_queue + playlist_unfetched
            if total_remaining > 0:
                message += f"<b>✨ {total_remaining} tracks still in the playlist.....</b>"

        return message'''

    pattern = r"    @staticmethod\n    def now_playing\(.*?return message"
    
    if re.search(pattern, code, flags=re.DOTALL):
        code = re.sub(pattern, new_func, code, flags=re.DOTALL)
        with open(msg_file, "w", encoding="utf-8") as f:
            f.write(code)
        print("✅ messages.py perfect ho gaya (Raw String used)!")
    else:
        print("❌ now_playing function nahi mila.")
cat << 'EOF' > fix_small.py
import os, re

file = "sunlomusic/ui/messages.py"
if os.path.exists(file):
    with open(file, "r", encoding="utf-8") as f: code = f.read()

    nl = chr(10)
    lines = [
        "    @staticmethod",
        "    def now_playing(track: Dict, requested_by: str = \"Unknown\", current_time: int = 0, queue: List[Dict] = None, playlist_unfetched: int = 0) -> str:",
        "        title = track.get('title', 'Unknown')",
        f"        message = \"<emoji id='5334665104677941170'>🎵</emoji> <b>Music Playlist:</b>{nl}{nl}\"",
        "        req_id = track.get('requested_by_id')",
        "        if req_id:",
        "            req_mention = f'<a href=\"tg://user?id={req_id}\">{requested_by}</a>'",
        "        else:",
        "            req_mention = requested_by",
        f"        message += f\"<b>1. <emoji id='5222472119295684375'>🎸</emoji> {title}</b>{nl}\"",
        f"        message += f\"<emoji id='5944970130554359187'>🏆</emoji> <b>Requested by:</b> {req_mention}{nl}{nl}\"",
        "        if queue and len(queue) > 1:",
        "            for i, next_track in enumerate(queue[1:4], start=2):",
        "                next_title = next_track.get('title', 'Unknown')",
        "                if len(next_title) > 50:",
        "                    next_title = next_title[:47] + \"...\"",
        "                next_name = next_track.get('requested_by', 'Unknown')",
        "                next_id = next_track.get('requested_by_id')",
        "                if next_id:",
        "                    next_mention = f'<a href=\"tg://user?id={next_id}\">{next_name}</a>'",
        "                else:",
        "                    next_mention = next_name",
        f"                message += f\"<b>{i}. <emoji id='5222472119295684375'>🎸</emoji> {next_title}</b>{nl}\"",
        f"                message += f\"<emoji id='5944970130554359187'>🏆</emoji> <b>Requested by:</b> {next_mention}{nl}{nl}\"",
        "            shown = min(len(queue), 4)",
        "            remaining_in_queue = len(queue) - shown",
        "            total_remaining = remaining_in_queue + playlist_unfetched",
        "            if total_remaining > 0:",
        f"                message += f\"<b>✨ {total_remaining} tracks still in the playlist.....</b>\"",
        "        return message"
    ]
    new_func = "\n".join(lines)
    code = re.sub(r"    @staticmethod\n    def now_playing\(.*?return message", new_func, code, flags=re.DOTALL)
    with open(file, "w", encoding="utf-8") as f: f.write(code)
    print("✅ messages.py fixed perfectly!")
else:
    print("❌ File not found!")

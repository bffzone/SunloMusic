# Copyright (C) @YO_UR_OFFICIAL_CRUSH

from typing import Dict, List

class Messages:
    @staticmethod
    def now_playing(track: Dict, requested_by: str = "Unknown", current_time: int = 0, queue: List[Dict] = None, playlist_unfetched: int = 0) -> str:
        title = track.get('title', 'Unknown')
        message = "<emoji id='5334665104677941170'>🎵</emoji> <b>Music Playlist:</b>" + chr(10) + chr(10)
        req_id = track.get('requested_by_id')
        if req_id:
            req_mention = f'<a href="tg://user?id={req_id}">{requested_by}</a>'
        else:
            req_mention = requested_by
        message += f"<b>1. <emoji id='5222472119295684375'>🎸</emoji> {title}</b>" + chr(10)
        message += f"<emoji id='5944970130554359187'>🏆</emoji> <b>Requested by:</b> {req_mention}" + chr(10) + chr(10)
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
                message += f"<b>{i}. <emoji id='5222472119295684375'>🎸</emoji> {next_title}</b>" + chr(10)
                message += f"<emoji id='5944970130554359187'>🏆</emoji> <b>Requested by:</b> {next_mention}" + chr(10) + chr(10)
            shown = min(len(queue), 4)
            remaining_in_queue = len(queue) - shown
            total_remaining = remaining_in_queue + playlist_unfetched
            if total_remaining > 0:
                message += f"<b>✨ {total_remaining} tracks still in the playlist.....</b>"
        return message

    @staticmethod
    def start_welcome(user_name: str = "User") -> str:
        return f"""<b>✨ Welcome to SunloMusic, {user_name}! ✨</b>

<blockquote>🎧 <i>The most advanced music streaming bot for Telegram Voice Chats. Lag-free, high-quality, and fully equipped with AI tools.</i></blockquote>

🚀 <b>What can I do?</b>
» <b>Ultra-Fast Streaming:</b> Crystal clear 320kbps audio.
» <b>Smart Playback:</b> Auto-play, Loop & Queue system.
» <b>Media Downloader:</b> Save restricted files easily.
» <b>AI & Utilities:</b> AI Chat, Temp Mail, Stylish Names.

👇 <i>Click the buttons below to explore!</i>"""

    HELP_BASIC = [
        ("/start", "Show welcome message"),
        ("/help", "Show this help message"),
        ("/status", "Show bot statistics"),
        ("/rank or /ranking", "View group rankings"),
        ("/tmail", "Generate a temporary email"),
        ("/cmail <token>", "Check temporary email inbox"),
        ("/gem <prompt>", "Ask Gemini AI anything"),
        ("/imgai <prompt>", "Reply to a photo for AI analysis"),
        ("/dl <link>", "Download private/restricted content"),
        ("/love <name1> <name2>", "Calculate Love Percentage"),
        ("/couple on/off", "Toggle auto best couple award"),
    ]
    HELP_MUSIC = [
        ("/play <query>", "Play a song from YouTube"),
        ("/pause", "Pause current playback"),
        ("/resume", "Resume playback"),
        ("/skip", "Skip to next track"),
        ("/stop", "Stop and leave voice chat"),
        ("/playlist", "View current queue"),
        ("/clearplaylist", "Clear upcoming tracks"),
        ("/seek <seconds>", "Seek forward/backward"),
        ("/rewind", "Rewind 10 seconds"),
    ]
    HELP_SETTINGS = [
        ("/settings", "Configure bot settings"),
        ("/vcadmin", "Add voice chat admin"),
        ("/vcunadmin", "Remove voice chat admin"),
    ]
    HELP_OWNER = [("/restart", "Restart the bot")]

    @staticmethod
    def help_rich(section: str = None):
        from pyrogram import types
        bold, code = types.RichTextBold, types.RichTextCode
        Block = types

        def cell(text, header=False):
            return Block.RichBlockTableCell(text, is_header=header, colspan=1, rowspan=1, align="left", valign="middle")

        def table(rows):
            body = [[cell("Command", True), cell("Description", True)]]
            body += [[cell(code(cmd)), cell(desc)] for cmd, desc in rows]
            return Block.InputRichBlockTable(body, is_bordered=True, is_striped=True, is_compact=False)

        def title(text):
            return [Block.InputRichBlockSectionHeading(text, size=1), Block.InputRichBlockDivider()]

        def heading(text):
            return Block.InputRichBlockSectionHeading(text, size=2)

        def para(*parts):
            return Block.InputRichBlockParagraph(list(parts) if len(parts) > 1 else parts[0])

        def quote(*parts):
            return Block.InputRichBlockBlockQuotation([Block.InputRichBlockParagraph(list(parts))])

        def item(*parts):
            return Block.InputRichBlockListItem(blocks=[Block.InputRichBlockParagraph(list(parts))])

        note = quote(bold("📌 Note"), ": Most commands work only in groups where the bot is admin.")

        if section == "basic":
            blocks = title("📖 Basic Commands") + [table(Messages.HELP_BASIC)]
        elif section == "music":
            blocks = title("🎶 Music Commands") + [
                para("(Use in groups)"),
                table(Messages.HELP_MUSIC),
                quote(bold("🎚 Effects"), ": Tap the ", bold("Effects"), " button on the player for ",
                      code("bassboost"), ", ", code("nightcore"), ", ", code("slowed"), ", ", code("lofi"), ", ",
                      code("8d"), " + speed control."),
            ]
        elif section == "settings":
            blocks = title("⚙️ Settings") + [
                para("(Admin only)"),
                table(Messages.HELP_SETTINGS),
                heading("Owner Commands"),
                table(Messages.HELP_OWNER),
                Block.InputRichBlockDivider(),
                note,
            ]
        else:
            blocks = title("🎵 SunloMusic Bot Commands") + [
                para("Pick a category below to see its commands."),
                Block.InputRichBlockList([
                    item(bold("Basic"), " — start, help, status and rankings"),
                    item(bold("Music"), " — playback, queue, seek and effects"),
                    item(bold("Settings"), " — admin tools and owner commands"),
                ]),
                Block.InputRichBlockDivider(),
                note,
            ]
        return Block.InputRichMessage(blocks=blocks)

    @staticmethod
    def help_message(section: str = None) -> str:
        def rows(items):
            return "\n".join(f"`{cmd}` - {desc}" for cmd, desc in items)

        note = "📌 **Note:** Most commands work only in groups where the bot is admin."
        if section == "basic":
            return f"📖 **Basic Commands**\n\n{rows(Messages.HELP_BASIC)}"
        if section == "music":
            return (
                f"🎶 **Music Commands** (Use in groups)\n\n{rows(Messages.HELP_MUSIC)}\n"
                "🎚 **Effects** - Tap the Effects button on the player for bassboost/nightcore/slowed/lofi/8d + speed control"
            )
        if section == "settings":
            return (
                f"⚙️ **Settings** (Admin only)\n\n{rows(Messages.HELP_SETTINGS)}\n\n"
                f"**Owner Commands:**\n{rows(Messages.HELP_OWNER)}\n\n{note}"
            )
        return (
            "<emoji id='5334665104677941170'>🎵</emoji> **SunloMusic Bot Commands**\n\n"
            "Pick a category below to see its commands.\n\n"
            "• **Basic** - start, help, status and rankings\n"
            "• **Music** - playback, queue, seek and effects\n"
            "• **Settings** - admin tools and owner commands\n\n"
            f"{note}"
        )

    @staticmethod
    def dm_not_allowed() -> str:
        return "Add me to a group to play music!"

    @staticmethod
    def status_message(total_users: int, total_groups: int, total_songs: int, active_vcs: int,
                       ping: float = None, cpu_usage: float = None) -> str:
        text = (
            f"📊 **Bot Usage Report**\n"
            f"━━━━━━━━━━━\n"
            f"**Total Users:** {total_users}\n"
            f"**Total Groups:** {total_groups}\n"
            f"**Total Songs Played:** {total_songs}\n"
            f"**Active Voice Chats:** {active_vcs}"
        )
        if ping is not None or cpu_usage is not None:
            text += "\n\n🛰 **Voice Engine**\n"
            if ping is not None:
                text += f"**Ping:** {ping:.1f} ms\n"
            if cpu_usage is not None:
                text += f"**CPU Usage:** {cpu_usage:.1f}%"
        return text

    @staticmethod
    def ranking_message(stats: Dict, period: str = "Daily") -> str:
        message = f"![🏆](tg://emoji?id=5944970130554359187) **Group Rankings - {period}**\n"
        message += "━━━━━━━━━━━━━━━━\n\n"

        if not stats or not stats.get('total_stats'):
            return message + "❌ No data available for this period."

        top_users = stats.get('top_users', [])
        top_songs = stats.get('top_songs', [])
        total_stats = stats.get('total_stats', {})

        if top_users:
            message += "👥 **Top 5 Users:**\n"
            for i, user in enumerate(top_users, 1):
                user_name = user['_id']['user_name']
                count = user['count']
                message += f"{i}. {user_name} - {count} songs\n"
            message += "\n"
        else:
            message += "👥 **Top 5 Users:**\nNo data available\n\n"

        if top_songs:
            message += "![🎵](tg://emoji?id=5334665104677941170) **Top 5 Songs:**\n"
            for i, song in enumerate(top_songs, 1):
                song_title = song['_id']
                if len(song_title) > 40:
                    song_title = song_title[:37] + "..."
                count = song['count']
                message += f"{i}. {song_title} - {count} plays\n"
            message += "\n"
        else:
            message += "![🎵](tg://emoji?id=5334665104677941170) **Top 5 Songs:**\nNo data available\n\n"

        message += "📊 **Stats:**\n"
        total_songs = total_stats.get('total_songs', 0)
        unique_users = len(total_stats.get('unique_users', []))
        total_duration = total_stats.get('total_duration', 0)

        hours = total_duration // 3600
        minutes = (total_duration % 3600) // 60

        message += f"Total Songs: {total_songs}\n"
        message += f"Active Users: {unique_users}\n"
        message += f"Listening Time: {hours}h {minutes}m\n"

        return message

    @staticmethod
    def global_ranking_message(stats: Dict) -> str:
        message = "🌍 **Global Rankings**\n"
        message += "━━━━━━━━━━━━━━━━\n\n"

        if not stats or not stats.get('total_stats'):
            return message + "❌ No data available."

        top_groups = stats.get('top_groups', [])
        top_users = stats.get('top_users', [])
        top_songs = stats.get('top_songs', [])
        total_stats = stats.get('total_stats', {})

        if top_groups:
            message += "![🏆](tg://emoji?id=5944970130554359187) **Top 5 Groups:**\n"
            for i, group in enumerate(top_groups, 1):
                chat_title = group.get('chat_title', 'Unknown Group')
                if len(chat_title) > 30:
                    chat_title = chat_title[:27] + "..."
                count = group['count']
                message += f"{i}. {chat_title} - {count} songs\n"
            message += "\n"
        else:
            message += "![🏆](tg://emoji?id=5944970130554359187) **Top 5 Groups:**\nNo data available\n\n"

        if top_users:
            message += "👥 **Top 5 Users:**\n"
            for i, user in enumerate(top_users, 1):
                user_name = user['_id']['user_name']
                count = user['count']
                message += f"{i}. {user_name} - {count} songs\n"
            message += "\n"
        else:
            message += "👥 **Top 5 Users:**\nNo data available\n\n"

        if top_songs:
            message += "![🎵](tg://emoji?id=5334665104677941170) **Top 5 Songs:**\n"
            for i, song in enumerate(top_songs, 1):
                song_title = song['_id']
                if len(song_title) > 40:
                    song_title = song_title[:37] + "..."
                count = song['count']
                message += f"{i}. {song_title} - {count} plays\n"
            message += "\n"
        else:
            message += "![🎵](tg://emoji?id=5334665104677941170) **Top 5 Songs:**\nNo data available\n\n"

        message += "📊 **Global Stats:**\n"
        total_songs = total_stats.get('total_songs', 0)
        unique_groups = len(total_stats.get('unique_groups', []))
        total_duration = total_stats.get('total_duration', 0)

        hours = total_duration // 3600
        minutes = (total_duration % 3600) // 60

        message += f"Total Songs: {total_songs}\n"
        message += f"Total Groups: {unique_groups}\n"
        message += f"Total Time: {hours}h {minutes}m\n"

        return message

messages = Messages()

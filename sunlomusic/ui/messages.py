# Copyright (C) @YO_UR_OFFICIAL_CRUSH

from typing import Dict, List

class Messages:
    @staticmethod
    def now_playing(track: Dict, requested_by: str = "Unknown", current_time: int = 0, queue: List[Dict] = None, playlist_unfetched: int = 0) -> str:
        title = track.get('title', 'Unknown')
        message = f"<emoji id='5334665104677941170'>🎵</emoji> <b>Music Playlist:</b>\n\n"

        req_id = track.get('requested_by_id')
        if req_id:
            req_mention = f"[{requested_by}](tg://user?id={req_id})"
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
                    next_mention = f"[{next_name}](tg://user?id={next_id})"
                else:
                    next_mention = next_name
                message += f"<b>{i}. <emoji id='5222472119295684375'>🎸</emoji> {next_title}</b>\n"
                message += f"<emoji id='5944970130554359187'>🏆</emoji> <b>Requested by:</b> {next_mention}\n\n"

            shown = min(len(queue), 4)
            remaining_in_queue = len(queue) - shown
            total_remaining = remaining_in_queue + playlist_unfetched
            if total_remaining > 0:
                message += f"<b>✨ {total_remaining} tracks still in the playlist.....</b>"

        return message

    @staticmethod
    def _create_progress_bar(current: int, total: int, length: int = 12) -> str:
        if total == 0:
            return "━" * length

        filled = int((current / total) * length)
        bar = "✦" * filled + "✧" * (length - filled)
        return bar

    @staticmethod
    def queue_list(queue: List[Dict], page: int = 0, page_size: int = 10) -> str:
        if not queue:
            return "📄 <b>Queue is empty</b>"

        start = page * page_size
        end = start + page_size
        page_queue = queue[start:end]

        message = f"📄 <b>Queue</b> ({len(queue)} tracks)\n\n"

        for i, track in enumerate(page_queue, start=start+1):
            title = track.get('title', 'Unknown')
            duration = Messages._format_duration(track.get('duration', 0))
            message += f"{i}. <b>{title}</b> `[{duration}]`\n"

        total_pages = (len(queue) + page_size - 1) // page_size
        message += f"\nPage {page+1}/{total_pages}"

        return message

    @staticmethod
    def settings_info(settings: Dict) -> str:
        message = "<emoji id='5316832430529722441'>⚙️</emoji> <b>Configure Your VCPlayer Settings Here.</b>\n"
        message += "━━━━━━━━━━━━━━━━━━━━━━━"

        return message

    @staticmethod
    def settings_rich(custom_emoji: bool = True):
        """Rich-message version of settings_info()."""
        from pyrogram import types
        icon = types.RichTextCustomEmoji("5316832430529722441", "⚙️") if custom_emoji else "⚙️"
        return types.InputRichMessage(blocks=[
            types.InputRichBlockParagraph([icon, " ", types.RichTextBold("Configure Your VCPlayer Settings Here.")]),
            types.InputRichBlockDivider(),
        ])

    @staticmethod
    def autoplay_prompt(seed_title: str) -> str:
        return (
            f"<emoji id='5334665104677941170'>🎧</emoji> <b>Playlist finished</b>\n\n"
            f"<b>Last played:</b> {seed_title}\n\n"
            f"Want me to keep the music going with related songs?"
        )

    @staticmethod
    def autoplay_prompt_rich(seed_title: str, custom_emoji: bool = True):
        """Rich "Playlist Finished" prompt asking whether to keep playing related songs."""
        from pyrogram import types

        icon = types.RichTextCustomEmoji("5316631095347788915", "🎵") if custom_emoji else "🎵"
        return types.InputRichMessage(blocks=[
            types.InputRichBlockSectionHeading([icon, " Playlist Finished"], size=1),
            types.InputRichBlockDivider(),
            types.InputRichBlockParagraph([types.RichTextBold("Last Played:"), f" {seed_title}"]),
            types.InputRichBlockDivider(),
            types.InputRichBlockBlockQuotation([
                types.InputRichBlockParagraph("Want me to keep the music going with related songs?")
            ]),
        ])

    @staticmethod
    def autoplay_searching() -> str:
        return (
            "<emoji id='5258396243666681152'>🔎</emoji> <b>Looking for related songs…</b>\n\n"
            "This may take a few seconds."
        )

    @staticmethod
    def autoplay_queued(count: int, seed_title: str) -> str:
        return (
            f"<emoji id='5334665104677941170'>🎧</emoji> <b>Autoplay on</b>\n\n"
            f"Queued <b>{count} related track(s)</b> based on <b>{seed_title}</b>."
        )

    @staticmethod
    def autoplay_queued_rich(count: int, seed_title: str, custom_emoji: bool = True):
        """Rich "Autoplay Status" message shown once related tracks are queued."""
        from pyrogram import types

        def emoji(emoji_id: str, alt: str):
            return types.RichTextCustomEmoji(emoji_id, alt) if custom_emoji else alt

        def stat(label, value):
            return types.InputRichBlockListItem(
                blocks=[types.InputRichBlockParagraph([types.RichTextBold(label), value])]
            )

        return types.InputRichMessage(blocks=[
            types.InputRichBlockSectionHeading([emoji("5222472119295684375", "🎶"), " Autoplay Status"], size=1),
            types.InputRichBlockDivider(),
            types.InputRichBlockParagraph([types.RichTextBold("Status:"), " On"]),
            types.InputRichBlockSectionHeading([emoji("5915480455603295660", "🎶"), " Queue Information"], size=3),
            types.InputRichBlockList([
                stat("Based On:", f" {seed_title}"),
                stat("Queued Tracks:", f" {count} related track(s)"),
            ]),
        ])

    @staticmethod
    def autoplay_unavailable() -> str:
        return (
            "❌ <b>No related songs found</b>\n\n"
            "Autoplay could not find anything to play next."
        )

    @staticmethod
    def autoplay_declined() -> str:
        return "⏹️ <b>Autoplay skipped</b> — playback stopped."

    @staticmethod
    def autoplay_expired() -> str:
        return "⌛️ <b>Autoplay request expired</b> — nobody answered, playback stopped."

    @staticmethod
    def vc_welcome(name: str = None) -> str:
        who = f", {name}" if name else ""
        return f"👋 Welcome{who}! Enjoy the music 🎶"

    @staticmethod
    def track_added(track: Dict, position: int) -> str:
        title = track.get('title', 'Unknown')
        return f"✅ Added to queue at position {position}\n<b>{title}</b>"

    @staticmethod
    def queue_updated(queue: List[Dict]) -> str:
        if not queue:
            return "📄 <b>Queue is empty</b>"

        duration = int(track.get('duration', 0))
        if duration > 0:
            bar = Messages._create_progress_bar(current_time, duration, length=10)
            current_str = Messages._format_duration(current_time)
            duration_str = Messages._format_duration(duration)
            timer = f"`{current_str}` {bar} `{duration_str}`"
        else:
            timer = "🔴 Live Stream"

        message = f"<emoji id='5334665104677941170'>🎵</emoji> <b>Music Playlist:</b>\n\n"
        message += f"{timer}\n\n"

        for i, track in enumerate(queue[:5], start=1):
            track_title = track.get('title', 'Unknown')
            if len(track_title) > 60:
                track_title = track_title[:57] + "..."
            req_name = track.get('requested_by', 'Unknown')
            req_id = track.get('requested_by_id')
            if req_id:
                req_mention = f"[{req_name}](tg://user?id={req_id})"
            else:
                req_mention = req_name
            message += f"<b>{i}. <emoji id='5222472119295684375'>🎸</emoji> {track_title}</b>\n"
            message += f"<emoji id='5944970130554359187'>🏆</emoji> <b>Requested by:</b> {req_mention}\n\n"

        if len(queue) > 5:
            remaining = len(queue) - 5
            message += f"<b>✨ {remaining} tracks still in the playlist.....</b>"

        return message

    @staticmethod
    def playlist_saved(name: str, count: int) -> str:
        return f"💾 Playlist <b>{name}</b> saved with {count} tracks"

    @staticmethod
    def playlist_loaded(name: str, count: int) -> str:
        return f"📀 Loaded playlist <b>{name}</b> with {count} tracks"

    @staticmethod
    def error(message: str) -> str:
        return f"❌ <b>Error:</b> {message}"

    @staticmethod
    def success(message: str) -> str:
        return f"✅ {message}"

    @staticmethod
    def _format_duration(seconds: int) -> str:
        if seconds == 0:
            return "Live"

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"

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

    @staticmethod
    def start_welcome_rich(custom_emoji: bool = True):
        """Rich-message version of start_welcome(). Falls back to plain emoji when custom emoji aren't wanted."""
        from pyrogram import types

        def emoji(emoji_id: str, alt: str):
            return types.RichTextCustomEmoji(emoji_id, alt) if custom_emoji else alt

        def feature(*parts):
            return types.InputRichBlockListItem(blocks=[types.InputRichBlockParagraph(list(parts))])

        bold = types.RichTextBold
        return types.InputRichMessage(blocks=[
            types.InputRichBlockSectionHeading([emoji("5316631095347788915", "🎵"), " Welcome to SunloMusic!"], size=1),
            types.InputRichBlockDivider(),
            types.InputRichBlockParagraph(bold("Your all-in-one voice chat player for music and video")),
            types.InputRichBlockSectionHeading([emoji("5316742794562254812", "✨"), " Key Features"], size=2),
            types.InputRichBlockList([
                feature(bold("Play Music & Videos")),
                feature(bold("Smooth Streaming")),
                feature(bold("Multi-Chat Support")),
                feature(bold("Full Controls"), " (pause, skip, seek, shuffle, replay)"),
                feature(bold("Audio & Video Modes")),
            ]),
            types.InputRichBlockDivider(),
            types.InputRichBlockParagraph([emoji("5316571734604790521", "🚀"), " ", bold("Choose an option below to get started!")]),
        ])

    @staticmethod
    def playlist_ready_rich(loaded: int, total: int, cap_note: str, first_track: str, custom_emoji: bool = True):
        """Rich "Playlist Ready" message shown after a playlist is loaded."""
        from pyrogram import types

        def emoji(emoji_id: str, alt: str):
            return types.RichTextCustomEmoji(emoji_id, alt) if custom_emoji else alt

        def stat(label, value):
            return types.InputRichBlockListItem(
                blocks=[types.InputRichBlockParagraph([types.RichTextBold(label), value])]
            )

        return types.InputRichMessage(blocks=[
            types.InputRichBlockSectionHeading([emoji("5316631095347788915", "🎵"), " Playlist Ready"], size=1),
            types.InputRichBlockDivider(),
            types.InputRichBlockSectionHeading("Status Update", size=2),
            types.InputRichBlockList([
                stat("Added to Queue:", f" {loaded} tracks"),
                stat("Playlist Contains:", f" {total} tracks{cap_note}"),
            ]),
            types.InputRichBlockDivider(),
            types.InputRichBlockSectionHeading([emoji("5850346984501680054", "▶️"), " First Track"], size=2),
            types.InputRichBlockParagraph(types.RichTextBold(first_track)),
        ])

    HELP_BASIC = [        ("/love <name1> <name2>", "Calculate Love Percentage"),
        ("/name <text>", "Generate stylish names"),

        ("/start", "Show welcome message"),
        ("/help", "Show this help message"),
        ("/status", "Show bot statistics"),
        ("/rank or /ranking", "View group rankings"),
        ("/tmail", "Generate a temporary email"),
        ("/cmail <token>", "Check temporary email inbox"),
        ("/gem <prompt>", "Ask Gemini AI anything"),
        ("/imgai <prompt>", "Reply to a photo for AI analysis"),
        ("/dl <link>", "Download private/restricted content"),
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
        """Rich help page. section: None (overview), 'basic', 'music' or 'settings'."""
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
        """Plain-text help page (fallback for help_rich)."""
        def rows(items):
            return "\n".join(f"`{cmd}` - {desc}" for cmd, desc in items)

        note = "📌 <b>Note:</b> Most commands work only in groups where the bot is admin."
        if section == "basic":
            return f"📖 <b>Basic Commands</b>\n\n{rows(Messages.HELP_BASIC)}"
        if section == "music":
            return (
                f"🎶 <b>Music Commands</b> (Use in groups)\n\n{rows(Messages.HELP_MUSIC)}\n"
                "🎚 <b>Effects</b> - Tap the Effects button on the player for bassboost/nightcore/slowed/lofi/8d + speed control"
            )
        if section == "settings":
            return (
                f"⚙️ <b>Settings</b> (Admin only)\n\n{rows(Messages.HELP_SETTINGS)}\n\n"
                f"<b>Owner Commands:</b>\n{rows(Messages.HELP_OWNER)}\n\n{note}"
            )
        return (
            "<emoji id='5334665104677941170'>🎵</emoji> <b>SunloMusic Bot Commands</b>\n\n"
            "Pick a category below to see its commands.\n\n"
            "• <b>Basic</b> - start, help, status and rankings\n"
            "• <b>Music</b> - playback, queue, seek and effects\n"
            "• <b>Settings</b> - admin tools and owner commands\n\n"
            f"{note}"
        )

    @staticmethod
    def dm_not_allowed() -> str:
        return "Add me to a group to play music!"

    @staticmethod
    def status_message(total_users: int, total_groups: int, total_songs: int, active_vcs: int,
                       ping: float = None, cpu_usage: float = None) -> str:
        text = (
            f"📊 <b>Bot Usage Report</b>\n"
            f"━━━━━━━━━━━\n"
            f"<b>Total Users:</b> {total_users}\n"
            f"<b>Total Groups:</b> {total_groups}\n"
            f"<b>Total Songs Played:</b> {total_songs}\n"
            f"<b>Active Voice Chats:</b> {active_vcs}"
        )
        if ping is not None or cpu_usage is not None:
            text += "\n\n🛰 <b>Voice Engine</b>\n"
            if ping is not None:
                text += f"<b>Ping:</b> {ping:.1f} ms\n"
            if cpu_usage is not None:
                text += f"<b>CPU Usage:</b> {cpu_usage:.1f}%"
        return text

    @staticmethod
    def ranking_message(stats: Dict, period: str = "Daily") -> str:
        message = f"<emoji id='5944970130554359187'>🏆</emoji> <b>Group Rankings - {period}</b>\n"
        message += "━━━━━━━━━━━━━━━━\n\n"

        if not stats or not stats.get('total_stats'):
            return message + "❌ No data available for this period."

        top_users = stats.get('top_users', [])
        top_songs = stats.get('top_songs', [])
        total_stats = stats.get('total_stats', {})

        if top_users:
            message += "👥 <b>Top 5 Users:</b>\n"
            for i, user in enumerate(top_users, 1):
                user_name = user['_id']['user_name']
                count = user['count']
                message += f"{i}. {user_name} - {count} songs\n"
            message += "\n"
        else:
            message += "👥 <b>Top 5 Users:</b>\nNo data available\n\n"

        if top_songs:
            message += "<emoji id='5334665104677941170'>🎵</emoji> <b>Top 5 Songs:</b>\n"
            for i, song in enumerate(top_songs, 1):
                song_title = song['_id']
                if len(song_title) > 40:
                    song_title = song_title[:37] + "..."
                count = song['count']
                message += f"{i}. {song_title} - {count} plays\n"
            message += "\n"
        else:
            message += "<emoji id='5334665104677941170'>🎵</emoji> <b>Top 5 Songs:</b>\nNo data available\n\n"

        message += "📊 <b>Stats:</b>\n"
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
        message = "🌍 <b>Global Rankings</b>\n"
        message += "━━━━━━━━━━━━━━━━\n\n"

        if not stats or not stats.get('total_stats'):
            return message + "❌ No data available."

        top_groups = stats.get('top_groups', [])
        top_users = stats.get('top_users', [])
        top_songs = stats.get('top_songs', [])
        total_stats = stats.get('total_stats', {})

        if top_groups:
            message += "<emoji id='5944970130554359187'>🏆</emoji> <b>Top 5 Groups:</b>\n"
            for i, group in enumerate(top_groups, 1):
                chat_title = group.get('chat_title', 'Unknown Group')
                if len(chat_title) > 30:
                    chat_title = chat_title[:27] + "..."
                count = group['count']
                message += f"{i}. {chat_title} - {count} songs\n"
            message += "\n"
        else:
            message += "<emoji id='5944970130554359187'>🏆</emoji> <b>Top 5 Groups:</b>\nNo data available\n\n"

        if top_users:
            message += "👥 <b>Top 5 Users:</b>\n"
            for i, user in enumerate(top_users, 1):
                user_name = user['_id']['user_name']
                count = user['count']
                message += f"{i}. {user_name} - {count} songs\n"
            message += "\n"
        else:
            message += "👥 <b>Top 5 Users:</b>\nNo data available\n\n"

        if top_songs:
            message += "<emoji id='5334665104677941170'>🎵</emoji> <b>Top 5 Songs:</b>\n"
            for i, song in enumerate(top_songs, 1):
                song_title = song['_id']
                if len(song_title) > 40:
                    song_title = song_title[:37] + "..."
                count = song['count']
                message += f"{i}. {song_title} - {count} plays\n"
            message += "\n"
        else:
            message += "<emoji id='5334665104677941170'>🎵</emoji> <b>Top 5 Songs:</b>\nNo data available\n\n"

        message += "📊 <b>Global Stats:</b>\n"
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

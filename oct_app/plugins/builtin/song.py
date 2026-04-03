from collections import defaultdict
import re

from ..base import ChatboxPlugin


def render_song(context, _text, data=0):
    if context["use_media_manager"]:
        try:
            current_media_info = context["get_media_info"]()
            artist = current_media_info["artist"]
            title = current_media_info["title"]
            album_title = current_media_info["album_title"]
            album_artist = current_media_info["album_artist"]
            media_playing = context["media_is"]("PLAYING")
        except Exception as e:
            artist = ""
            title = ""
            album_title = ""
            album_artist = ""
            media_playing = False
            if "TARGET_PROGRAM" not in str(e):
                try:
                    context["output_log"](f"mediaManagerError {e}")
                except Exception:
                    pass

        if context["remove_parenthesis"]:
            title = re.sub(r" ?\([^)]*\)", "", title)

        song_info = context["song_display"].format_map(
            defaultdict(
                str,
                artist=artist,
                title=title,
                album_title=album_title,
                album_artist=album_artist,
            )
        )
        if (not media_playing) and context["show_paused"]:
            song_info = song_info + " ⏸️"
    else:
        def format_time(seconds=0):
            minutes = int(seconds // 60)
            remaining_seconds = int(seconds % 60)
            return f"{minutes}:{remaining_seconds:02}"

        play_state = context.get("spotify_play_state")
        if play_state:
            try:
                artist = play_state.get("item").get("artists")[0].get("name")
                title = play_state.get("item").get("name")
                album_title = play_state.get("item").get("album").get("name")
                album_artist = play_state.get("item").get("artists")[0].get("name")
                song_progress = format_time(play_state.get("progress_ms") / 1000)
                song_length = format_time(play_state.get("item").get("duration_ms") / 1000)
                volume = str(play_state.get("device").get("volume_percent"))
                song_id = play_state.get("item").get("id")
                media_playing = play_state.get("is_playing")
            except Exception:
                artist = title = album_title = album_artist = ""
                song_progress = format_time(0)
                song_length = format_time(0)
                volume = "0"
                song_id = "N/A"
                media_playing = False
        else:
            artist = title = album_title = album_artist = ""
            song_progress = format_time(0)
            song_length = format_time(0)
            volume = "0"
            song_id = "N/A"
            media_playing = False

        if context["remove_parenthesis"]:
            title = re.sub(r" ?\([^)]*\)", "", title)

        song_info = context["spotify_song_display"].format_map(
            defaultdict(
                str,
                artist=artist,
                title=title,
                album_title=album_title,
                album_artist=album_artist,
                song_progress=song_progress,
                song_length=song_length,
                volume=volume,
                song_id=song_id,
            )
        )
        if (not media_playing) and context["show_paused"]:
            song_info = song_info + "⏸️"

    context["song_info"] = song_info

    try:
        if context["use_spotify_api"]:
            context["spotify_song_url"] = play_state.get("item").get("external_urls").get("spotify")
        else:
            context["spotify_song_url"] = ""
        # Song info is now sent via SocketIO status_update from the web module
        context["song_name"] = title + " \u1d47\u02b8 " + artist if title else ""
    except Exception:
        pass

    if (context["hide_song"] and not media_playing) or title == "":
        return ""

    if context["show_on_change"]:
        if song_info != context["song_name"]:
            context["tick_count"] = context["song_change_ticks"]
            context["song_name"] = song_info
        if context["tick_count"] != 0:
            context["tick_count"] = context["tick_count"] - 1
            return context["check_data"](song_info, data)
        return ""

    return context["check_data"](song_info, data)


plugin = ChatboxPlugin(name="song", render=render_song)

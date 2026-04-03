from ..base import ChatboxPlugin


def render_sparkle(context, text, data=0):
    frames_str = context.get("text_accent_frames", "✧,✦,★,☆,✶,✷")
    frames = [f.strip() for f in frames_str.split(",") if f.strip()]
    if not frames:
        frames = ["✧"]

    idx = context.get("sparkle_frame_index", 0)
    accent = frames[idx % len(frames)]
    context["sparkle_frame_index"] = (idx + 1) % len(frames)

    result = text.replace("\\n", "\v").replace("\\v", "\v")
    rendered = f"{accent} {result} {accent}"
    return context["check_data"](rendered, data)


plugin = ChatboxPlugin(name="sparkle", render=render_sparkle)

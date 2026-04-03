from ..base import ChatboxPlugin

_frame_index = 0
_tick_counter = 0


def render_animate(context, _text, data=0):
    global _frame_index, _tick_counter
    frames_str = context.get("animate_frames", "[ Loading . ],[ Loading .. ],[ Loading ... ]")
    speed = context.get("animate_speed", 1)

    frames = [f.strip() for f in frames_str.split(",") if f.strip()]
    if not frames:
        return ""

    _tick_counter += 1
    if _tick_counter >= speed:
        _tick_counter = 0
        _frame_index = (_frame_index + 1) % len(frames)

    return context["check_data"](frames[_frame_index % len(frames)], data)


plugin = ChatboxPlugin(name="animate", render=render_animate)

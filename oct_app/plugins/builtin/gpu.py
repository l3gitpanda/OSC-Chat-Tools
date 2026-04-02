from collections import defaultdict

from ..base import ChatboxPlugin


def render_gpu(context, _text, data=0):
    try:
        from pynvml import nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates, nvmlInit, nvmlShutdown
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)
        info = nvmlDeviceGetUtilizationRates(handle)
        gpu_percent = info.gpu
        vram_percent = info.memory
        nvmlShutdown()
    except Exception:
        gpu_percent = "0"
        vram_percent = "0"

    gpu_data = context["gpu_display"].format_map(
        defaultdict(str, gpu_percent=gpu_percent, vram_percent=vram_percent)
    )
    return context["check_data"](gpu_data, data)


plugin = ChatboxPlugin(name="gpu", render=render_gpu)

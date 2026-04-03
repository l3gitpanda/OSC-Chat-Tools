from collections import defaultdict

from ..base import ChatboxPlugin

_nvml_initialized = False
_nvml_handle = None


def _ensure_nvml():
    global _nvml_initialized, _nvml_handle
    if not _nvml_initialized:
        from pynvml import nvmlDeviceGetHandleByIndex, nvmlInit
        nvmlInit()
        _nvml_handle = nvmlDeviceGetHandleByIndex(0)
        _nvml_initialized = True
    return _nvml_handle


def render_gpu(context, _text, data=0):
    try:
        from pynvml import nvmlDeviceGetUtilizationRates
        handle = _ensure_nvml()
        info = nvmlDeviceGetUtilizationRates(handle)
        gpu_percent = info.gpu
        vram_percent = info.memory
    except Exception:
        gpu_percent = "0"
        vram_percent = "0"

    gpu_data = context["gpu_display"].format_map(
        defaultdict(str, gpu_percent=gpu_percent, vram_percent=vram_percent)
    )
    return context["check_data"](gpu_data, data)


plugin = ChatboxPlugin(name="gpu", render=render_gpu)

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Dict


@dataclass
class AppConfig:
    conf_version: str = "2.0.0"
    message_delay: float = 1.5
    message_string: str = ""
    osc_listen_address: str = "127.0.0.1"
    osc_listen_port: int = 9001
    osc_send_address: str = "127.0.0.1"
    osc_send_port: int = 9000
    osc_forward_address: str = "127.0.0.1"
    osc_forward_port: int = 9002
    use_spotify_api: bool = False
    use_pulsoid: bool = True
    use_hyperate: bool = False


def migrate_config(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize legacy `osc-chat-tools.py` key names into package config names."""

    key_map = {
        "messageString": "message_string",
        "message_delay": "message_delay",
        "oscListenAddress": "osc_listen_address",
        "oscListenPort": "osc_listen_port",
        "oscSendAddress": "osc_send_address",
        "oscSendPort": "osc_send_port",
        "oscForewordAddress": "osc_forward_address",
        "oscForewordPort": "osc_forward_port",
        "useSpotifyApi": "use_spotify_api",
        "usePulsoid": "use_pulsoid",
        "useHypeRate": "use_hyperate",
        "confVersion": "conf_version",
    }

    migrated: Dict[str, Any] = {}
    for k, v in raw.items():
        migrated[key_map.get(k, k)] = v
    return migrated


def load_config(path: str | Path) -> AppConfig:
    cfg_path = Path(path)
    if not cfg_path.exists():
        return AppConfig()
    raw = json.loads(cfg_path.read_text(encoding="utf-8"))
    migrated = migrate_config(raw)
    defaults = asdict(AppConfig())
    defaults.update({k: v for k, v in migrated.items() if k in defaults})
    return AppConfig(**defaults)


def save_config(path: str | Path, config: AppConfig) -> None:
    cfg_path = Path(path)
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    cfg_path.write_text(json.dumps(asdict(config), indent=2), encoding="utf-8")

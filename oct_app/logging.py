from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Optional


@dataclass
class ThreadSafeLogger:
    """Simple thread-safe logger used by OCT modules."""

    logfile: Optional[Path] = None
    enabled: bool = True
    _lock: Lock = field(default_factory=Lock, init=False, repr=False)

    def log(self, message: str) -> None:
        if not self.enabled:
            return
        line = f"{datetime.now().isoformat(sep=' ', timespec='seconds')} {message}"
        with self._lock:
            print(line)
            if self.logfile is not None:
                self.logfile.parent.mkdir(parents=True, exist_ok=True)
                with self.logfile.open("a", encoding="utf-8") as f:
                    f.write(line + "\n")

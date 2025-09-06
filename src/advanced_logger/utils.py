

from pathlib import Path
import os

def ensure_path(path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

def is_log_file(path: str | Path) -> bool:
    return '.log' in os.path.splitext(path)

def is_json_file(path: str | Path) -> bool:
    return '.json' in os.path.splitext(path)
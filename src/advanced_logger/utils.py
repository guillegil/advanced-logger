

from pathlib import Path
import os

def ensure_path(path: str | Path) -> None:
    try:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
    except (OSError, PermissionError) as e:
        raise RuntimeError(f"Failed to create path {path}: {e}")

def is_log_file(path: str | Path) -> bool:
    return '.log' in os.path.splitext(path)

def is_json_file(path: str | Path) -> bool:
    return '.json' in os.path.splitext(path)
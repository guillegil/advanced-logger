import logging

from colored import Fore as fg
from colored import Style as st

COLOR_RESET = st.RESET

DEFAULT_LEVEL_KEY   : str = 'info'
DEFAULT_LEVEL_NAME  : str = 'INFO'
DEFAULT_LEVELNO     : int = logging.INFO
DEFAULT_LEVEL_COLOR : str = fg.WHITE

_LEVELS = {
    "debug"     : {"levelno": logging.DEBUG,    "color": fg.CYAN,         "name": "DEBUG"     },
    "info"      : {"levelno": logging.INFO,     "color": fg.WHITE,        "name": "INFO"      },
    "warning"   : {"levelno": logging.WARNING,  "color": fg.YELLOW,       "name": "WARNING"   },
    "error"     : {"levelno": logging.ERROR,    "color": fg.RED,          "name": "ERROR"     },
    "critical"  : {"levelno": logging.CRITICAL, "color": fg.RED,          "name": "CRITICAL"  },
    "step"      : {"levelno": 21,               "color": fg.WHITE,        "name": "STEP"      },
    "substep"   : {"levelno": 22,               "color": fg.light_gray,   "name": "SUBSTEP"   },
    "pass"      : {"levelno": 23,               "color": fg.GREEN,        "name": "PASS"      },
    "fail"      : {"levelno": 31,               "color": fg.RED,          "name": "FAIL"      },
}

def _normalize_level(level_id: str) -> str:
    level_id = level_id.replace(' ', '')
    level_id = level_id.replace('_', '')
    level_id = level_id.replace('-', '')
    level_id = level_id.lower()

    return level_id

def get_level_number(level_id: str) -> int:
    if isinstance(level_id, int):
        return level_id
    
    level_id = _normalize_level(level_id)
    return _LEVELS.get(level_id, {}).get('levelno', DEFAULT_LEVELNO)

def get_level_name(level_id: str) -> int:
    level_id = _normalize_level(level_id)
    return _LEVELS.get(level_id, {}).get('name', DEFAULT_LEVEL_NAME)

def get_level_color(level_id: str) -> str:
    level_id = _normalize_level(level_id)
    return _LEVELS.get(level_id, {}).get('color', DEFAULT_LEVEL_COLOR)

def get_level_name_by_number(levelno: int) -> str:
    for level_key, _ in _LEVELS.items():
        if get_level_number(level_key) == levelno:
            return get_level_name(level_key)
    
    return DEFAULT_LEVEL_NAME

def get_level_color_by_number(levelno: int) -> str:
    for level_key, _ in _LEVELS.items():
        if get_level_number(level_key) == levelno:
            return get_level_color(level_key)
    
    return DEFAULT_LEVEL_COLOR

def get_level_number_by_name(level_name: str) -> int:
    for level_key, level_info in _LEVELS.items():
        if level_info['name'] == level_name:
            return get_level_number(level_key)
    
    return DEFAULT_LEVELNO


def get_level(level_id: str | int) -> int|str:
    if isinstance(level_id, str):
        normalized_level = _normalize_level(level_id)
        if normalized_level not in _LEVELS:
            return get_level_number_by_name(normalized_level)
        else: 
            return get_level_number(level_id)
    elif isinstance(level_id, int):
        return get_level_name_by_number(level_id)
    else:
        # -- Maybe it's time to show a warning here... ------------------------- #
        return DEFAULT_LEVEL_NAME

def add_new_level(level_id: str):
    logging.addLevelName(get_level_number(level_id), get_level_name(level_id))

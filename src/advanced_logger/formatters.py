from logging import Formatter

from .levels import COLOR_RESET
from .levels import             \
    get_level_number,           \
    get_level_name,             \
    get_level_name_by_number,   \
    get_level_color_by_number,  \
    add_new_level                     


class FileFormatter(Formatter):

    def __init__(
        self, 
        fmt      : str = None,
        datefmt  : str = None,
        style    : str = '%',
    ):
        if fmt is None:
            fmt = "[%(asctime)s] %(levelname)-8s %(message)s"
     
        # -- Register custom levels ------------------------------------ #
        add_new_level('step')
        add_new_level('substep')
        add_new_level('passed')
        add_new_level('failed')

        super().__init__(fmt, datefmt, style)

    def format(self, record):
        # -- Extract level info ------------------------------ #
        levelname: str = record.levelname
        levelno: int = record.levelno

        # -- Get original formatted message ------------------ #
        formatted = super().format(record)

        # -- Add indentation for substep --------------------------- #
        if get_level_name_by_number(levelno) == get_level_name('substep'):
            formatted = "   " + formatted

        return f"{formatted}"

class ColorFormatter(Formatter):

    def __init__(
        self, 
        fmt      : str = None,
        datefmt  : str = None,
        style    : str = '%',
    ):
        if fmt is None:
            fmt = "[%(asctime)s] %(levelname)-8s %(message)s"
     
        # -- Register custom levels ------------------------------------ #
        add_new_level('step')
        add_new_level('substep')
        add_new_level('passed')
        add_new_level('failed')

        super().__init__(fmt, datefmt, style)

    def format(self, record):
        # -- Extract level info ------------------------------ #
        levelname: str = record.levelname
        levelno: int = record.levelno

        # -- Get original formatted message ------------------ #
        formatted = super().format(record)

        # -- Add indentation for substep --------------------- #
        # -- Add indentation for substep --------------------------- #
        if get_level_name_by_number(levelno) == get_level_name('substep'):
            formatted = "   " + formatted

        # -- Wrap the entire line in color, then reset ------- #
        color: str = get_level_color_by_number(levelno)
        return f"{color}{formatted}{COLOR_RESET}"

class ProcedureFormater(Formatter):

    def __init__(
        self, 
        fmt     : str = None,
        datefmt : str = None, 
        style   : str = '%'
    ):
        if fmt is None:
            fmt = "[%(asctime)s] %(levelname)-8s %(message)s"

        # -- Register custom levels ---------------------- #
        add_new_level('step')
        add_new_level('substep')

        super().__init__(fmt, datefmt, style)

    def format(self, record):
        # -- Extract level info ------------------------------------ #
        levelname: str = record.levelname
        levelno: int = record.levelno

        # -- Get original formatted message ------------------------ # 
        formatted = super().format(record)

        # -- Add indentation for substep --------------------------- #
        if get_level_name_by_number(levelno) == get_level_name('substep'):
            formatted = "   " + formatted

        return formatted
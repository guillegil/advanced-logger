
from logging import Filter

from .levels import get_level_number

class StepOnlyFilter(Filter):
    """Filter that only allows step and substep log records through"""
    def filter(self, record):
        return record.levelno in [get_level_number('step'), get_level_number('substep')]
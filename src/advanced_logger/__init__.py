from .advanced_logger import AdvancedLogger

log = AdvancedLogger('default_logger', init_default_term_handler=True)

__all__ = ["AdvancedLogger", "log"]
__version__ = "0.2.0"
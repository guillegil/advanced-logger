

from advanced_logger import log

def test_logger():
    from advanced_logger import AdvancedLogger

    assert isinstance(log, AdvancedLogger), f'log, is not instance of a TestLogger class. log is {type(log)}'
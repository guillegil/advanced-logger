

from advanced_logger import log

def test_logger():
    from advanced_logger import AdvancedLogger

    assert isinstance(log, AdvancedLogger), f'log, is not instance of a TestLogger class. log is {type(log)}'

def test_logger_name():
    assert 'default_logger' == log.name, f'Log name does not match the global one, got {log.name}'


from testlogger import log

def test_logger():
    from testlogger import TestLogger

    assert isinstance(log, TestLogger), f'log, is not instance of a TestLogger class. log is {type(log)}'
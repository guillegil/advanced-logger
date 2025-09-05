
from advanced_logger import log

def test_debug_logs(caplog):
    with caplog.at_level(log.DEBUG):
        log.debug('This is an debug message')

    assert 'This is an debug message' in caplog.text, f'Terminal output log is not as expected, got "{caplog.text}"'

def test_info_logs(caplog):
    with caplog.at_level(log.INFO):
        log.info('This is an info message')

    assert 'This is an info message' in caplog.text, f'Terminal output log is not as expected, got {caplog.text}'


def test_warning_logs(caplog):
    with caplog.at_level(log.WARNING):
        log.warning('This is an warning message')

    assert 'This is an warning message' in caplog.text, f'Terminal output log is not as expected, got "{caplog.text}"'


def test_error_logs(caplog):
    with caplog.at_level(log.ERROR):
        log.error('This is an error message')

    assert 'This is an error message' in caplog.text, f'Terminal output log is not as expected, got "{caplog.text}"'
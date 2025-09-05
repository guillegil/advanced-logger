
import pytest

from advanced_logger import log

import sys
from io import StringIO
from contextlib import contextmanager

@contextmanager
def capture_stdout():
    old_stdout = sys.stdout
    captured_output = StringIO()
    sys.stdout = captured_output
    try:
        yield captured_output
    finally:
        sys.stdout = old_stdout

def test_debug_logs(caplog):    
    with capture_stdout() as captured:
        with caplog.at_level(log.DEBUG):
            log.debug('This is a funny log 🤣')
            log.debug('This debug', 'message', 'was', 'build', 'with multiple', 'strings')
            log.debug('This', 'debug', 'message', 'is', '-', 'separated', sep='-')
            log.debug('This', 'debug', 'message', 'is', '🐍', 'separated', sep='🐍')
            log.debug('This debug should not be printed', enable=False)

    assert 'This is a funny log 🤣' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This debug message was build with multiple strings' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This-debug-message-is---separated' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This🐍debug🐍message🐍is🐍🐍🐍separated' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This debug should not be printed' not in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'


def test_info_logs(caplog):
    with caplog.at_level(log.INFO):
        log.info('This is an info message ℹ️')
        log.info('This info', 'message', 'was', 'build', 'with multiple', 'strings')
        log.info('This', 'info', 'message', 'is', '-', 'separated', sep='-')
        log.info('This', 'info', 'message', 'is', '🐍', 'separated', sep='🐍')
        log.info('This info should not be printed', enable=False)

    assert 'This is an info message ℹ️' in caplog.text, f'Captured log is not as expected, got {caplog.text}'
    assert 'This info message was build with multiple strings' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This-info-message-is---separated' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This🐍info🐍message🐍is🐍🐍🐍separated' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This info should not be printed' not in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'

    log_path = "./reports/test_info_logs"

def test_warning_logs(caplog):
    with caplog.at_level(log.WARNING):
        log.warning('This is an warning message ⚠️')
        log.warning('This warning', 'message', 'was', 'build', 'with multiple', 'strings')
        log.warning('This', 'warning', 'message', 'is', '-', 'separated', sep='-')
        log.warning('This', 'warning', 'message', 'is', '🐍', 'separated', sep='🐍')
        log.warning('This warning should not be printed', enable=False)

    assert 'This is an warning message ⚠️' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This warning message was build with multiple strings' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This-warning-message-is---separated' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This🐍warning🐍message🐍is🐍🐍🐍separated' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This warning should not be printed' not in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'

def test_error_logs(caplog):
    with caplog.at_level(log.ERROR):
        log.error('This is an error message ☠️')
        log.error('This error', 'message', 'was', 'build', 'with multiple', 'strings')
        log.error('This', 'error', 'message', 'is', '-', 'separated', sep='-')
        log.error('This', 'error', 'message', 'is', '🐍', 'separated', sep='🐍')
        log.error('This error should not be printed', enable=False)

    assert 'This is an error message ☠️' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This error message was build with multiple strings' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This-error-message-is---separated' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This🐍error🐍message🐍is🐍🐍🐍separated' in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
    assert 'This error should not be printed' not in caplog.text, f'Captured log is not as expected, got "{caplog.text}"'
from advanced_logger import log
from advanced_logger.levels import _LEVELS

from logging import Handler

def test_log_properties():
    assert hasattr(log, 'DEBUG')
    assert hasattr(log, 'INFO')
    assert hasattr(log, 'WARNING')
    assert hasattr(log, 'ERROR')
    assert hasattr(log, 'CRITICAL')
    assert hasattr(log, 'STEP')
    assert hasattr(log, 'SUBSTEP')
    assert hasattr(log, 'PASS')
    assert hasattr(log, 'FAIL')

    assert log.DEBUG    == _LEVELS['debug']['levelno']
    assert log.INFO     == _LEVELS['info']['levelno']
    assert log.WARNING  == _LEVELS['warning']['levelno']
    assert log.ERROR    == _LEVELS['error']['levelno']
    assert log.CRITICAL == _LEVELS['critical']['levelno']
    assert log.STEP     == _LEVELS['step']['levelno']
    assert log.SUBSTEP  == _LEVELS['substep']['levelno']
    assert log.FAIL     == _LEVELS['fail']['levelno']
    assert log.PASS     == _LEVELS['pass']['levelno']

def test_handler_properties():
    assert hasattr(log, 'active_handlers')

    assert 'stage_handler' in log.active_handlers
    assert isinstance(log.active_handlers['stage_handler'], Handler)
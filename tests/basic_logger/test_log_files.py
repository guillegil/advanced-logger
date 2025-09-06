import pytest

from advanced_logger import log
from advanced_logger.levels import get_level_name

@pytest.mark.parametrize(
    "level,message",
    [
        ("debug", "This is a debug message"),
        ("info", "This is an info message"),
        ("warning", "This is a warning message"),
        ("error", "This is an error message"),
        ("critical", "This is a critical message"),
        ("step", "This is a step message"),
        ("substep", "This is a substep message"),
        ("pass", "This test passed"),
        ("fail", "This test failed"),
    ]
)
def test_log_files(call_log_file, level, message):

    log.log(level, message, extra={'step': ''})

    # Read the log file and verify the message was written
    with open(call_log_file, 'r') as fd:
        log_content = fd.read()
        log_content.replace('\n', '')
    
    levelname: str = get_level_name(level)
    if level != 'substep':
        assert f"[{levelname}] - {message}" in log_content
    else:
        assert f"   [{levelname}] - {message}" in log_content
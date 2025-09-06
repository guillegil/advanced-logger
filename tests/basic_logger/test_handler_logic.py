from advanced_logger import log 
import pytest
import os

def test_correct_path(setup_log_file, call_log_file, procedure_json_file, procedure_log_file):
    log.init_procedure_log_handler('procedure_handler_correct_path', procedure_log_file)
    log.export_procedure_json(procedure_json_file)

    assert os.path.exists(setup_log_file)
    assert os.path.exists(call_log_file)
    assert os.path.exists(procedure_json_file)
    assert os.path.exists(procedure_log_file)

    log.remove_handler('procedure_handler_correct_path')

@pytest.mark.parametrize(
    "level",
    [
        (log.DEBUG),
        (log.INFO),
        (log.WARNING),
        (log.ERROR),
        (log.CRITICAL),
        (log.FAIL),
        (log.PASS),
        (log.STEP),
        (log.SUBSTEP),
    ]
)
def test_handler_use(level):
    assert 'stage_handler' in log.active_handlers

    handler = log.init_file_handler('dummy_handler', './reports/dummy.log', level=level)

    assert 'dummy_handler' in log.active_handlers
    assert log.active_handlers['dummy_handler'] == handler
    assert handler.level == level

    log.log(level, f"This message with level: {level} must be logged !!", extra={"step": ""})

    with open('./reports/dummy.log', 'r') as dummy_log_fd:
        dummy_log = dummy_log_fd.read()
        assert f"This message with level: {level} must be logged !!" in dummy_log

    log.remove_handler('dummy_handler')

    assert 'dummy_handler' not in log.active_handlers

    for _, handler_object in log.active_handlers.items():
        assert handler_object != handler
    
    log.log(level, f"This message with level: {level} shoudn't be logged !!", extra={"step": ""})

    with open('./reports/dummy.log', 'r') as dummy_log:
        assert f"This message with level: {level} shoudn't be logged !!" not in dummy_log
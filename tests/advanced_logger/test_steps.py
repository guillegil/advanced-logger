

import sys
from advanced_logger import log

def test_step_log(caplog):

    with caplog.at_level(log.STEP):
        log.step('This is the first step')  # 1.
        log.step('This is the second')      # 2.
        log.substep('This is a substep')    # 2.1.
        log.substep('This is a substep')    # 2.2
        log.substep('This is a substep')    # 2.3
        log.step('another step')            # 3.
        log.substep('another substep')      # 3.1

    assert 'This is the first step' in caplog.text
    assert 'This is the second' in caplog.text
    assert 'This is a substep' in caplog.text
    assert 'This is a substep' in caplog.text
    assert 'This is a substep' in caplog.text
    assert 'another step' in caplog.text
    assert 'another substep' in caplog.text

def test_step_count():

    assert log.stepn == 0 and log.substepn == 0
    log.step('This is the first step')  # 1.
    assert log.stepn == 1 and log.substepn == 0
    log.step('This is the second')      # 2.
    assert log.stepn == 2 and log.substepn == 0
    log.substep('This is a substep')    # 2.1.
    assert log.stepn == 2 and log.substepn == 1
    log.substep('This is a substep')    # 2.2
    assert log.stepn == 2 and log.substepn == 2
    log.substep('This is a substep')    # 2.3
    assert log.stepn == 2 and log.substepn == 3
    log.step('another step')            # 3.
    assert log.stepn == 3 and log.substepn == 0
    log.substep('another substep')      # 3.1
    assert log.stepn == 3 and log.substepn == 1

    log.reset_steps()

    assert log.stepn == 0 and log.substepn == 0
    log.step('This is the first step')  # 1.
    assert log.stepn == 1 and log.substepn == 0
    log.step('This is the second')      # 2.
    assert log.stepn == 2 and log.substepn == 0
    log.substep('This is a substep')    # 2.1.
    assert log.stepn == 2 and log.substepn == 1
    log.substep('This is a substep')    # 2.2
    assert log.stepn == 2 and log.substepn == 2
    log.substep('This is a substep')    # 2.3
    assert log.stepn == 2 and log.substepn == 3
    log.step('another step')            # 3.
    assert log.stepn == 3 and log.substepn == 0
    log.substep('another substep')      # 3.1
    assert log.stepn == 3 and log.substepn == 1
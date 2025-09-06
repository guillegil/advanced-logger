from advanced_logger import log

def test_fail_pass(caplog):
    with caplog.at_level(log.FAIL):
        log.fail('This is a failure from a fail log')
    
    assert 'This is a failure from a fail log' in caplog.text

    with caplog.at_level(log.PASS):
        log.passed('This is a passed from a passed log')

    assert 'This is a passed from a passed log' in caplog.text
    
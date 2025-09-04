

from testlogger import log

def test_logger():
    log.init_term_handler()
    log.init_call_logger('./reports/test_logger.log')

    log.info("Hello from the logger")


test_logger()
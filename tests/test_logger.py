

from testlogger import log

def test_logger():
    log.init_term_handler('term_handler', level='debug')
    log.init_file_handler('test', './reports/test_logger.log')
    log.init_procedure_log_handler('procedure', './reports/test_procedure.log')

    log.debug("This is a debug")
    log.info("Hello from the logger")
    log.warning("This is warning")
    log.error("This is an error")
    log.step("This is a step")
    log.substep("This is a substep")
    log.substep("This is a substep")
    log.substep("This is a substep")
    log.step("This is a step")
    log.substep("This is a substep")
    log.substep("This is a substep")
    log.substep("This is a substep")

    log.fail("This failed")
    log.passed("This passed")


    log.export_procedure_json('./reports/procedure.json')

test_logger()



import pytest
from pytest import Item

from advanced_logger import log
from pytest_meta import meta

import os

REPORTS_PATH = './reports'

def pytest_runtest_setup(item: Item):
    print()
    setup_log_path = os.path.join(REPORTS_PATH, meta.nodeid, f"{meta.testindex}", 'setup', f"setup_{meta.testcase}.log")
    log.init_term_handler('term_handler', level='debug')
    log.init_file_handler('setup_handler', setup_log_path, level='debug')


def pytest_runtest_call(item: Item):
    call_log_path = os.path.join(REPORTS_PATH, meta.testcase, f"{meta.testindex}", f"{meta.testcase}.log")

    log.remove_handler('setup_handler')
    log.init_file_handler('call_handler', call_log_path, level='debug')



import pytest
from pytest import Item

from advanced_logger import log
from pytest_meta import meta

import os

REPORTS_PATH = './reports'

def get_test_path() -> str:
    return os.path.join(REPORTS_PATH, meta.nodeid, f"{meta.testindex}")

def gen_setup_log_file() -> str:
    return os.path.join(get_test_path(), 'setup', f"setup_{meta.testcase}.log")

def gen_call_log_file() -> str:
    return os.path.join(get_test_path(), f"{meta.testcase}.log")

def gen_test_procedure_log_file() -> str:
    return os.path.join(get_test_path(), f"procedure.log")

def gen_test_procedure_json_file() -> str:
    return os.path.join(get_test_path(), f"procedure.json")


@pytest.fixture
def setup_log_file() -> str:
    yield gen_setup_log_file()

@pytest.fixture
def call_log_file() -> str:
    yield gen_call_log_file()

@pytest.fixture
def procedure_log_file() -> str:
    yield gen_test_procedure_log_file()

@pytest.fixture
def procedure_json_file() -> str:
    yield gen_test_procedure_json_file()

def pytest_runtest_setup(item: Item):
    print()
    log.set_logger_level('debug')
    log.init_term_handler('default_term_logger', level=log.DEBUG)
    log.init_file_handler('stage_handler', gen_setup_log_file(), level='debug')


def pytest_runtest_call(item: Item):
    log.reset_steps()
    log.init_file_handler('stage_handler', gen_call_log_file(), level='debug')
    log.init_procedure_log_handler('procedure_log', gen_test_procedure_log_file())


def pytest_runtest_logreport():
    pass
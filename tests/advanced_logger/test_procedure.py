from advanced_logger import log
import json

expected_procedure_log = [
    "1. Initialize environment and load test configuration",
    "   1.1. Load environment variables from config file",
    "      1.1.1. Read .env file",
    "      1.1.2. Parse environment variables",
    "      1.1.3. Validate required variables exist",
    "   1.2. Validate mandatory configuration keys are present",
    "   1.3. Establish initial database connection",
    "      1.3.1. Connect to database server",
    "      1.3.2. Verify database schema version",
    "2. Start the core application service",
    "   2.1. Launch background worker process",
    "      2.1.1. Initialize worker thread pool",
    "      2.1.2. Start message queue consumer",
    "   2.2. Verify service is listening on expected port",
    "   2.3. Check that startup logs contain no errors",
    "3. Execute main workflow scenario",
    "   3.1. Send mock API request with valid payload",
    "   3.2. Validate system's response matches schema",
    "      3.2.1. Check HTTP status code == 200",
    "      3.2.2. Validate JSON against schema validator",
    "      3.2.3. Verify response headers are correct",
    "   3.3. Confirm record was written into database",
    "   3.4. Trigger downstream notification handler",
    "4. Test error handling paths",
    "   4.1. Send malformed API request to trigger 400 error",
    "   4.2. Confirm error response contains proper message",
    "   4.3. Inject artificial DB outage and retry workflow",
    "      4.3.1. Kill database container",
    "      4.3.2. Retry main workflow, expect DB error",
    "      4.3.3. Restart database container",
    "   4.4. Ensure system gracefully recovers when DB is restored",
    "5. Clean up and teardown environment",
    "   5.1. Terminate background worker process",
    "   5.2. Drop temporary test database tables",
    "   5.3. Remove test configuration files",
    "      5.3.1. Delete temporary config files",
    "      5.3.2. Clear environment variables",
    "   5.4. Release memory and close all connections",
]

def do_log_procedure():
    # (step_count).(substep_count).(subsubstep_count)
    log.step("Initialize environment and load test configuration")      # 1.
    log.substep("Load environment variables from config file")          # 1.1
    log.substep("Read .env file", is_substep=True)                      # 1.1.1
    log.substep("Parse environment variables", is_substep=True)         # 1.1.2
    log.substep("Validate required variables exist", is_substep=True)   # 1.1.3
    log.substep("Validate mandatory configuration keys are present")    # 1.2
    log.substep("Establish initial database connection")                # 1.3
    log.substep("Connect to database server", is_substep=True)          # 1.3.1
    log.substep("Verify database schema version", is_substep=True)      # 1.3.2

    log.step("Start the core application service")                      # 2.
    log.substep("Launch background worker process")                     # 2.1
    log.substep("Initialize worker thread pool", is_substep=True)       # 2.1.1
    log.substep("Start message queue consumer", is_substep=True)        # 2.1.2
    log.substep("Verify service is listening on expected port")         # 2.2
    log.substep("Check that startup logs contain no errors")            # 2.3

    log.step("Execute main workflow scenario")                          # 3.
    log.substep("Send mock API request with valid payload")             # 3.1
    log.substep("Validate system's response matches schema")            # 3.2
    log.substep("Check HTTP status code == 200", is_substep=True)       # 3.2.1
    log.substep("Validate JSON against schema validator", is_substep=True) # 3.2.2
    log.substep("Verify response headers are correct", is_substep=True) # 3.2.3
    log.substep("Confirm record was written into database")             # 3.3
    log.substep("Trigger downstream notification handler")              # 3.4

    log.step("Test error handling paths")                               # 4.
    log.substep("Send malformed API request to trigger 400 error")      # 4.1
    log.substep("Confirm error response contains proper message")       # 4.2
    log.substep("Inject artificial DB outage and retry workflow")       # 4.3
    log.substep("Kill database container", is_substep=True)             # 4.3.1
    log.substep("Retry main workflow, expect DB error", is_substep=True) # 4.3.2
    log.substep("Restart database container", is_substep=True)          # 4.3.3
    log.substep("Ensure system gracefully recovers when DB is restored") # 4.4

    log.step("Clean up and teardown environment")                       # 5.
    log.substep("Terminate background worker process")                  # 5.1
    log.substep("Drop temporary test database tables")                  # 5.2
    log.substep("Remove test configuration files")                      # 5.3
    log.substep("Delete temporary config files", is_substep=True)       # 5.3.1
    log.substep("Clear environment variables", is_substep=True)         # 5.3.2
    log.substep("Release memory and close all connections")             # 5.4


def test_procedure(procedure_log_file):

    do_log_procedure()

    with open(procedure_log_file, 'r') as fd:
        for index, line in enumerate(fd):
            line = line.replace('\n', '')
            assert line in expected_procedure_log[index]


expected_procedure_by_id = {
    '1':     {'id': '1',     'parent': None,  'description': 'Initialize environment and load test configuration'},
    '1.1':   {'id': '1.1',   'parent': '1',   'description': 'Load environment variables from config file'},
    '1.1.1': {'id': '1.1.1', 'parent': '1.1', 'description': 'Read .env file'},
    '1.1.2': {'id': '1.1.2', 'parent': '1.1', 'description': 'Parse environment variables'},
    '1.1.3': {'id': '1.1.3', 'parent': '1.1', 'description': 'Validate required variables exist'},
    '1.2':   {'id': '1.2',   'parent': '1',   'description': 'Validate mandatory configuration keys are present'},
    '1.3':   {'id': '1.3',   'parent': '1',   'description': 'Establish initial database connection'},
    '1.3.1': {'id': '1.3.1', 'parent': '1.3', 'description': 'Connect to database server'},
    '1.3.2': {'id': '1.3.2', 'parent': '1.3', 'description': 'Verify database schema version'},
    '2':     {'id': '2',     'parent': None,  'description': 'Start the core application service'},
    '2.1':   {'id': '2.1',   'parent': '2',   'description': 'Launch background worker process'},
    '2.1.1': {'id': '2.1.1', 'parent': '2.1', 'description': 'Initialize worker thread pool'},
    '2.1.2': {'id': '2.1.2', 'parent': '2.1', 'description': 'Start message queue consumer'},
    '2.2':   {'id': '2.2',   'parent': '2',   'description': 'Verify service is listening on expected port'},
    '2.3':   {'id': '2.3',   'parent': '2',   'description': 'Check that startup logs contain no errors'},
    '3':     {'id': '3',     'parent': None,  'description': 'Execute main workflow scenario'},
    '3.1':   {'id': '3.1',   'parent': '3',   'description': 'Send mock API request with valid payload'},
    '3.2':   {'id': '3.2',   'parent': '3',   'description': "Validate system's response matches schema"},
    '3.2.1': {'id': '3.2.1', 'parent': '3.2', 'description': 'Check HTTP status code == 200'},
    '3.2.2': {'id': '3.2.2', 'parent': '3.2', 'description': 'Validate JSON against schema validator'},
    '3.2.3': {'id': '3.2.3', 'parent': '3.2', 'description': 'Verify response headers are correct'},
    '3.3':   {'id': '3.3',   'parent': '3',   'description': 'Confirm record was written into database'},
    '3.4':   {'id': '3.4',   'parent': '3',   'description': 'Trigger downstream notification handler'},
    '4':     {'id': '4',     'parent': None,  'description': 'Test error handling paths'},
    '4.1':   {'id': '4.1',   'parent': '4',   'description': 'Send malformed API request to trigger 400 error'},
    '4.2':   {'id': '4.2',   'parent': '4',   'description': 'Confirm error response contains proper message'},
    '4.3':   {'id': '4.3',   'parent': '4',   'description': 'Inject artificial DB outage and retry workflow'},
    '4.3.1': {'id': '4.3.1', 'parent': '4.3', 'description': 'Kill database container'},
    '4.3.2': {'id': '4.3.2', 'parent': '4.3', 'description': 'Retry main workflow, expect DB error'},
    '4.3.3': {'id': '4.3.3', 'parent': '4.3', 'description': 'Restart database container'},
    '4.4':   {'id': '4.4',   'parent': '4',   'description': 'Ensure system gracefully recovers when DB is restored'},
    '5':     {'id': '5',     'parent': None,  'description': 'Clean up and teardown environment'},
    '5.1':   {'id': '5.1',   'parent': '5',   'description': 'Terminate background worker process'},
    '5.2':   {'id': '5.2',   'parent': '5',   'description': 'Drop temporary test database tables'},
    '5.3':   {'id': '5.3',   'parent': '5',   'description': 'Remove test configuration files'},
    '5.3.1': {'id': '5.3.1', 'parent': '5.3', 'description': 'Delete temporary config files'},
    '5.3.2': {'id': '5.3.2', 'parent': '5.3', 'description': 'Clear environment variables'},
    '5.4':   {'id': '5.4',   'parent': '5',   'description': 'Release memory and close all connections'},
}

def test_procedure_json(procedure_json_file):

    do_log_procedure()

    log.export_procedure_json(procedure_json_file)

    with open(procedure_json_file, 'r') as file:
        data: dict = json.load(file)
        
        assert 'steps' in data

        steps: list[dict] = data['steps']

        for _, step in enumerate(steps):
            assert 'id' in step
            assert 'description' in step
            assert 'parent' in step

        for id, stepinfo in expected_procedure_by_id.items():
            logstep = list(filter(lambda step: step['id'] == id, steps))

            assert logstep != []
            assert len(logstep) == 1

            logstep_item: dict = logstep[0]

            assert stepinfo['description'] in logstep_item['description']
            assert stepinfo['parent'] == logstep_item['parent']
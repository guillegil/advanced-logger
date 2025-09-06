from advanced_logger import log
import json

expected_procedure_log = [
    "1. Initialize environment and load test configuration",
    "   1.1. Load environment variables from config file",
    "   1.2. Validate mandatory configuration keys are present",
    "   1.3. Establish initial database connection",
    "2. Start the core application service",
    "   2.1. Launch background worker process",
    "   2.2. Verify service is listening on expected port",
    "   2.3. Check that startup logs contain no errors",
    "3. Execute main workflow scenario",
    "   3.1. Send mock API request with valid payload",
    "   3.2. Validate system’s response matches schema",
    "   3.3. Confirm record was written into database",
    "   3.4. Trigger downstream notification handler",
    "4. Test error handling paths",
    "   4.1. Send malformed API request to trigger 400 error",
    "   4.2. Confirm error response contains proper message",
    "   4.3. Inject artificial DB outage and retry workflow",
    "   4.4. Ensure system gracefully recovers when DB is restored",
    "5. Clean up and teardown environment",
    "   5.1. Terminate background worker process",
    "   5.2. Drop temporary test database tables",
    "   5.3. Remove test configuration files",
    "   5.4. Release memory and close all connections",
]

def do_log_procedure():
    # (step_count).(substep_count)
    log.step("Initialize environment and load test configuration")      # 1.
    log.substep("Load environment variables from config file")          # 1.1
    log.substep("Validate mandatory configuration keys are present")    # 1.2
    log.substep("Establish initial database connection")                # 1.3

    log.step("Start the core application service")                      # 2.
    log.substep("Launch background worker process")                     # 2.1
    log.substep("Verify service is listening on expected port")         # 2.2
    log.substep("Check that startup logs contain no errors")            # 2.3

    log.step("Execute main workflow scenario")                          # 3.
    log.substep("Send mock API request with valid payload")             # 3.1
    log.substep("Validate system’s response matches schema")            # 3.2
    log.substep("Confirm record was written into database")             # 3.3
    log.substep("Trigger downstream notification handler")              # 3.4

    log.step("Test error handling paths")                               # 4.
    log.substep("Send malformed API request to trigger 400 error")      # 4.1
    log.substep("Confirm error response contains proper message")       # 4.2
    log.substep("Inject artificial DB outage and retry workflow")       # 4.3
    log.substep("Ensure system gracefully recovers when DB is restored")# 4.4

    log.step("Clean up and teardown environment")                       # 5.
    log.substep("Terminate background worker process")                  # 5.1
    log.substep("Drop temporary test database tables")                  # 5.2
    log.substep("Remove test configuration files")                      # 5.3
    log.substep("Release memory and close all connections")             # 5.4



def test_procedure(procedure_log_file):

    do_log_procedure()

    with open(procedure_log_file, 'r') as fd:
        for index, line in enumerate(fd):
            line = line.replace('\n', '')
            assert line == expected_procedure_log[index]


 
expected_procedure_by_id = {
    '1':   {'id': '1',   'parent': None, 'description': 'Initialize environment and load test configuration'},
    '1.1': {'id': '1.1', 'parent': '1',  'description': 'Load environment variables from config file'},
    '1.2': {'id': '1.2', 'parent': '1',  'description': 'Validate mandatory configuration keys are present'},
    '1.3': {'id': '1.3', 'parent': '1',  'description': 'Establish initial database connection'},
    '2':   {'id': '2',   'parent': None, 'description': 'Start the core application service'},
    '2.1': {'id': '2.1', 'parent': '2',  'description': 'Launch background worker process'},
    '2.2': {'id': '2.2', 'parent': '2',  'description': 'Verify service is listening on expected port'},
    '2.3': {'id': '2.3', 'parent': '2',  'description': 'Check that startup logs contain no errors'},
    '3':   {'id': '3',   'parent': None, 'description': 'Execute main workflow scenario'},
    '3.1': {'id': '3.1', 'parent': '3',  'description': 'Send mock API request with valid payload'},
    '3.2': {'id': '3.2', 'parent': '3',  'description': "Validate system’s response matches schema"},
    '3.3': {'id': '3.3', 'parent': '3',  'description': 'Confirm record was written into database'},
    '3.4': {'id': '3.4', 'parent': '3',  'description': 'Trigger downstream notification handler'},
    '4':   {'id': '4',   'parent': None, 'description': 'Test error handling paths'},
    '4.1': {'id': '4.1', 'parent': '4',  'description': 'Send malformed API request to trigger 400 error'},
    '4.2': {'id': '4.2', 'parent': '4',  'description': 'Confirm error response contains proper message'},
    '4.3': {'id': '4.3', 'parent': '4',  'description': 'Inject artificial DB outage and retry workflow'},
    '4.4': {'id': '4.4', 'parent': '4',  'description': 'Ensure system gracefully recovers when DB is restored'},
    '5':   {'id': '5',   'parent': None, 'description': 'Clean up and teardown environment'},
    '5.1': {'id': '5.1', 'parent': '5',  'description': 'Terminate background worker process'},
    '5.2': {'id': '5.2', 'parent': '5',  'description': 'Drop temporary test database tables'},
    '5.3': {'id': '5.3', 'parent': '5',  'description': 'Remove test configuration files'},
    '5.4': {'id': '5.4', 'parent': '5',  'description': 'Release memory and close all connections'},
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

            assert stepinfo['description'] == logstep_item['description']
            assert stepinfo['parent'] == logstep_item['parent']

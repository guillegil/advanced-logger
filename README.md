# Advanced Logger

A lightweight and flexible logging utility designed to simplify logging in Python applications. It provides a clean interface for quick logging.

## 🚀 Getting Started

### Quick Example
```python
from advanced_logger import log

log.info("Hello, world!")
# Output: [INFO] - Hello, world!
```
### Creating a Custom Logger

```python
from advanced_logger import AdvancedLogger

log = AdvancedLogger("mylogger")
log.init_term_handler('my_term_handler', level='info')

log.debug("Hello my logger!")
log.info("Hello my logger!")
log.warning("Hello my logger!")
log.error("Hello my logger!")
log.critical("Hello my logger!")
```

### Using test-oriented logs

```python
from advanced_logger import AdvancedLogger

log = AdvancedLogger("mylogger")
log.init_term_handler('my_term_handler') # INFO as default
 
log.debug("Hello my logger!")
log.info("Hello my logger!")
log.warning("Hello my logger!")
log.error("Hello my logger!")
log.critical("Hello my logger!")
```

### Available logging methods

```python
from advanced_logger import log

log = AdvancedLogger("mylogger")
log.init_term_handler('my_term_handler') # INFO as default
log.init_procedure_log_handler('myprocedure', './procedure.log')

log.step("Start the core application service")
log.substep("Launch background worker process")
log.substep("Verify service is listening on expected port")
log.substep("Check that startup logs contain no errors")
log.step("Execute main workflow scenario")
log.substep("Send mock API request with valid payload")
log.substep("Validate system’s response matches schema")
log.substep("Confirm record was written into database")
log.substep("Trigger downstream notification handler")

# -- Generated termianl log ---------------------------------------- #
#
# [STEP 1] - Start the core application service
#    [SUBSTEP 1.1] - Launch background worker process
#    [SUBSTEP 1.2] - Verify service is listening on expected port
#    [SUBSTEP 1.3] - Check that startup logs contain no errors
# [STEP 2] - Execute main workflow scenario
#    [SUBSTEP 2.1] - Send mock API request with valid payload
#    [SUBSTEP 2.2] - Validate system’s response matches schema
#    [SUBSTEP 2.3] - Confirm record was written into database
#    [SUBSTEP 2.4] - Trigger downstream notification handler

# -- Generated procedure log @ ./procedure.log --------------------- #
#
# 1. Start the core application service,
#    1.1. Launch background worker process,
#    1.2. Verify service is listening on expected port,
#    1.3. Check that startup logs contain no errors,
# 2. Execute main workflow scenario,
#    2.1. Send mock API request with valid payload,
#    2.2. Validate system’s response matches schema,
#    2.3. Confirm record was written into database,
#    2.4. Trigger downstream notification handler,
```

## 🔧 Development Setup

If you want to contribute or work with this repository:

1. Create and activate a virtual environment

```bash
python -m venv venv

source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate     # On Windows
```

1. Install the package in editable mode with dependencies
   
```bash
pip install -e .
```

3. Additionally, install `pytest` and [pytest_meta](https://github.com/guillegil/pytest-meta) for testing.

```python
pip install pytest git+https://github.com/guillegil/pytest-meta@develop
```

# 📚 Notes

- The default `log` instance is pre-configured for terminal reporting for quick testing and small scripts.
- Use `AdvancedLogger` when you need custom log names, multiple loggers, or project-level configuration.
- Compatible with Python’s built-in logging ecosystem, so you can integrate it seamlessly with larger projects.
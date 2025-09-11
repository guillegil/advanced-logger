
import json

import logging
from logging import Logger, Handler


from typing import Optional


from .utils import *
from .basic_logger import BasicLogger
from .formatters import ProcedureFormater
from .levels import add_new_level, get_level_number
from .filter import StepOnlyFilter

datefmt = "%Y-%m-%d %H:%M:%S"





class AdvancedLogger(BasicLogger):
    _instances: dict[str, "AdvancedLogger"] = {}

    def __new__(
        cls: "AdvancedLogger", 
        logger_name: str = "default",
        *args,
        **kwargs
    ) -> "AdvancedLogger":
        if logger_name in cls._instances:
            return cls._instances[logger_name]
        
        instance = super().__new__(cls)
        cls._instances[logger_name] = instance

        return instance

    def __init__(
        self, 
        logger_name: str = "advanced_logger_instance",
        *args,
        **kwargs
    ):
        if getattr(self, "_init_done", False):
            return
        
        super().__init__(logger_name, args, kwargs)
        self._init_done = True

        add_new_level('step')
        add_new_level('substep')
        add_new_level('pass')
        add_new_level('fail')

        self.__test_procedure: dict = {
            'test_id': "",
            'description': "",
            'steps': []
        }

        # -- Step count for the step log --------------------------- #
        self.__stepn    : int = 0
        # -- The substep one --------------------------------------- #
        self.__substepn : int = 0
    

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # -- Cleanup handlers ------------------------------------- #
        for handler_name in list(self.active_handlers.keys()):
            self.remove_handler(handler_name)

    # =============================================
    #          TEST LEVELS PROPERTIES
    # =============================================

    @property
    def STEP(self) -> int:
        return get_level_number('step')

    @property
    def SUBSTEP(self) -> int:
        return get_level_number('substep')

    @property
    def PASS(self) -> int:
        return get_level_number('pass')

    @property
    def FAIL(self) -> int:
        return get_level_number('fail')

    @property
    def test_procedure(self) -> dict:
        return self.__test_procedure

    @property
    def stepn(self) -> int:
        return self.__stepn

    @property
    def substepn(self) -> int:
        return self.__substepn
    
    @property
    def logger(self) -> Logger:
        return super().logger

    @staticmethod
    def has_instance(logger_name: str) -> bool:
        return logger_name in AdvancedLogger._instances

    # ============================================================================
    #                              LOGGER METHODS
    # ============================================================================

    def init_term_handler(
        self, 
        handler_name: str,
        level: str|int = 'info',
        fmt = '%(indent)s[%(levelname)s%(step)s] - %(message)s'
    ):
        return super().init_term_handler(handler_name, level, fmt)

    def init_file_handler(
        self, 
        handler_name, 
        path, 
        level = 'info', 
        fmt = '%(indent)s[%(levelname)s%(step)s] - %(message)s',
        mode = 'w',
        encoding = 'utf-8'
    ):
        return super().init_file_handler(handler_name, path, level, fmt, mode, encoding)

    def init_procedure_log_handler(
        self,
        handler_name    : str,
        path            : str,
        fmt             : Optional[str] = '%(step)s. %(message)s',  # Simple format for procedure log
        mode            : Optional[str] = 'w',
        encoding        : Optional[str] = 'utf-8'
    ) -> Handler:
        """Initialize a handler that only logs step and substep messages"""
        
        ensure_path(path)
        
        # Create file handler
        handler = self._create_file_handler(path, mode=mode, encoding=encoding)
        
        # Set level to capture both step and substep (use the lower level)
        self.set_handler_level(handler, self.STEP)
        
        # Add the step-only filter
        handler.addFilter( StepOnlyFilter() )
        
        # Set formatter (no timestamp/level needed for procedure log)
        handler.setFormatter( ProcedureFormater(fmt=fmt, datefmt=datefmt)  )
        
        # Add to logger
        self._add_handler(handler_name, handler)
        
        return handler
 
    def reset_steps(self) -> None:
        self.__stepn = 0
        self.__substepn = 0

        self.__test_procedure: dict = {
            'test_id': "",
            'description': "",
            'steps': [],
            'procedure_info': {}
        }


    # ============================================================================
    #                             EXPORT METHODS
    # ============================================================================

    def export_procedure_json(self, path: str) -> None:
        ensure_path(path)

        # Open the file in write mode ('w')
        with open(path, 'w') as json_file:
            json.dump(self.__test_procedure, json_file, indent=4)


    # ============================================================================
    #                               LOGS METHODS
    # ============================================================================

    def debug(self, *args, sep=' ', end='', enable=True, **kwargs):
        super().debug(*args, sep=sep, end=end, enable=enable)

    def info(self, *args, sep=' ', end='', enable=True):
        super().info(*args, sep=sep, end=end, enable=enable)

    def warning(self, *args, sep=' ', end='', enable=True):
        super().warning(*args, sep=sep, end=end, enable=enable)

    def error(self, *args, sep=' ', end='', enable=True, **kwargs):
        super().error(*args, sep=sep, end=end, enable=enable)

    def critical(self, *args, sep=' ', end='', enable=True, **kwargs):
        super().critical(*args, sep=sep, end=end, enable=enable)

    def passed(self, *args, sep=' ', end='', enable=True, **kwargs):
        indent :str = " "*kwargs.get('indent', 0)
        extra = {"step": "", "indent": indent}

        if enable and args: 
            msg = sep.join(str(a) for a in args) + end

            # Apply indent to every line in the message
            msg = ''.join(part if i == 0 else indent + part
              for i, part in enumerate(msg.splitlines(keepends=True)))

            # Correctly call the logger.info method
            self.log(self.PASS, msg, extra=extra)

    def fail(self, *args, sep=' ', end='', enable=True, **kwargs):
        indent:str  = " "*kwargs.get('indent', 0)
        extra = {"step": "", "indent": indent}

        if enable and args: 
            msg = sep.join(str(a) for a in args) + end

            msg = ''.join(part if i == 0 else indent + part
              for i, part in enumerate(msg.splitlines(keepends=True)))

            # Correctly call the logger.info method
            self.log(self.FAIL, msg, extra=extra)

    def step(self, *args, sep=' ', end='', enable=True, **kwargs):
        self.__stepn += 1
        self.__substepn = 0

        indent :str = " "*kwargs.get('indent', 0)
        extra = {"step": f"{self.__stepn}", "indent": indent}

        if enable and args: 
            msg = sep.join(str(a) for a in args) + end

            msg = ''.join(part if i == 0 else indent + part
              for i, part in enumerate(msg.splitlines(keepends=True)))

            # Correctly call the logger.info method
            self.log(self.STEP, msg, extra=extra)

        procedure_info = kwargs.get('procedure_info', {})

        self.__test_procedure['steps'].append({
            'id': f"{self.__stepn}",
            'parent': None,
            'description': sep.join(str(a) for a in args) + end,
            'procedure_info': procedure_info
        })

    def substep(self, *args, sep=' ', end='', enable=True, **kwargs):
        self.__substepn += 1

        indent :str = " "*kwargs.get('indent', 0)
        extra = {"step": f"{self.__stepn}.{self.__substepn}", "indent": indent}

        if enable and args: 
            msg = sep.join(str(a) for a in args) + end

            msg = ''.join(part if i == 0 else indent + part
              for i, part in enumerate(msg.splitlines(keepends=True)))

            # Correctly call the logger.info method
            self.log(self.SUBSTEP, msg, extra=extra)

        procedure_info = kwargs.get('procedure_info', {})

        self.__test_procedure['steps'].append({
            'id': f"{self.__stepn}.{self.__substepn}",
            'parent': f"{self.__stepn}",
            'description': sep.join(str(a) for a in args) + end,
            'procedure_info': procedure_info
        }) 
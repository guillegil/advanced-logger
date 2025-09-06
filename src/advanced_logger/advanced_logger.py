
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
    
    def __init__(
        self, 
        logger_name: str = "advanced_logger_instance",
        *args,
        **kwargs
    ):
        super().__init__(logger_name, args, kwargs)

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

    # ============================================================================
    #                              LOGGER METHODS
    # ============================================================================
    
    def init_term_handler(
        self, 
        handler_name: str,
        level: str|int = 'info',
        fmt = '[%(levelname)s%(step)s] - %(message)s'
    ):
        return super().init_term_handler(handler_name, level, fmt)

    def init_file_handler(
        self, 
        handler_name, 
        path, 
        level = 'info', 
        fmt = '[%(levelname)s%(step)s] - %(message)s',
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
            'steps': []
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
        if 'extra' not in kwargs:
            kwargs['extra'] = {}

        kwargs['extra']['step'] = kwargs['extra'].get('step', '')

        super().debug(*args, sep=sep, end=end, enable=enable, **kwargs)

    def info(self, *args, sep=' ', end='', enable=True, **kwargs):
        if 'extra' not in kwargs:
            kwargs['extra'] = {}

        kwargs['extra']['step'] = kwargs['extra'].get('step', '')

        super().info(*args, sep=sep, end=end, enable=enable, **kwargs)

    def warning(self, *args, sep=' ', end='', enable=True, **kwargs):
        if 'extra' not in kwargs:
            kwargs['extra'] = {}

        kwargs['extra']['step'] = kwargs['extra'].get('step', '')

        super().warning(*args, sep=sep, end=end, enable=enable, **kwargs)

    def error(self, *args, sep=' ', end='', enable=True, **kwargs):
        if 'extra' not in kwargs:
            kwargs['extra'] = {}

        kwargs['extra']['step'] = kwargs['extra'].get('step', '')

        super().error(*args, sep=sep, end=end, enable=enable, **kwargs)

    def critical(self, *args, sep=' ', end='', enable=True, **kwargs):
        if 'extra' not in kwargs:
            kwargs['extra'] = {}

        kwargs['extra']['step'] = kwargs['extra'].get('step', '')

        super().critical(*args, sep=sep, end=end, enable=enable, **kwargs)

    def passed(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = {"step": ""}

        if enable and args: 
            msg = sep.join(str(a) for a in args) + end
            # Correctly call the logger.info method
            self.log(self.PASS, msg, **kwargs, extra=extra)

    def fail(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = {"step": ""}

        if enable and args:
            msg = sep.join(str(a) for a in args) + end
            self.log(self.FAIL, msg, **kwargs, extra=extra)
    
    def step(self, *args, sep=' ', end='', enable=True, **kwargs):
        self.__stepn += 1
        self.__substepn = 0

        extra = {"step": f"{self.__stepn}"}

        if enable and args:  # Only log if enabled and there are arguments
            msg = sep.join(str(a) for a in args) + end
            # Correctly call the logger.info method
            self.log(self.STEP, msg, **kwargs, extra=extra)

        self.__test_procedure['steps'].append({
            'id': f"{self.__stepn}",
            'parent': None,
            'description': sep.join(str(a) for a in args) + end
        })

    def substep(self, *args, sep=' ', end='', enable=True, **kwargs):
        self.__substepn += 1

        extra = {"step": f"{self.__stepn}.{self.__substepn}"}

        if enable and args:  # Only log if enabled and there are arguments
            msg = sep.join(str(a) for a in args) + end
            self.log(self.SUBSTEP, msg, **kwargs, extra=extra)

        self.__test_procedure['steps'].append({
            'id': f"{self.__stepn}.{self.__substepn}",
            'parent': f"{self.__stepn}",
            'description': sep.join(str(a) for a in args) + end
        }) 
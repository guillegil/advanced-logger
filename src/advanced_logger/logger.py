
import json

from logging import Logger, Handler

import logging

import sys
from typing import Optional, Union

from pathlib import Path
from .formatters import ColorFormatter, ProcedureFormater
from .levels import get_level_number, get_level

datefmt = "%Y-%m-%d %H:%M:%S"



class StepOnlyFilter(logging.Filter):
    """Filter that only allows step and substep log records through"""
    def filter(self, record):
        return record.levelno in [get_level_number('step'), get_level_number('substep')]

class AdvancedLogger:
    
    def __init__(
        self, 
        logger_name: str = "advanced_logger_instance",
        *args,
        **kwargs
    ):
        self.__logger : Logger = logging.getLogger( logger_name )
        print(f"{self.INFO=}")
        self.__logger.setLevel( self.INFO )

        self.__active_handlers: dict[str, Handler] = {}

        self.__test_procedure: dict = {
            'test_id': "",
            'description': "",
            'steps': []
        }

        # -- Step count for the step log --------------------------- #
        self.__stepn    : int = 0
        # -- The substep one --------------------------------------- #
        self.__substepn : int = 0
    
    @property
    def DEBUG(self) -> int:
        return get_level_number('debug')

    @property
    def INFO(self) -> int:
        return get_level_number('info')

    @property
    def WARNING(self) -> int:
        return get_level_number('warning')

    @property
    def ERROR(self) -> int:
        return get_level_number('error')

    @property
    def CRITICAL(self) -> int:
        return get_level_number('critical')

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
    def logger(self) -> Logger:
        return self.__logger

    @property
    def test_procedure(self) -> dict:
        return self.__test_procedure

    @property
    def stepn(self) -> int:
        return self.__stepn

    @property
    def substepn(self) -> int:
        return self.__substepn

    # ============================================================================
    #                              PRIVATE METHODS
    # ============================================================================

    def __map_level(self, level : Union[str, int]) -> int:
        return get_level(level)

    def __add_handler(self, handler_name: str, handler: Handler) -> None:
        # -- Remove to avoid duplicates ------------------ #
        self.__remove_handler(handler_name)

        self.__logger.addHandler( handler )
        self.__active_handlers[handler_name] = handler

    def __remove_handler(self, handler_identifier: Union[str, Handler]) -> None:
        """Remove a handler by name (string) or by handler object"""
        
        if isinstance(handler_identifier, str):
            # -- Remove by name ----------------------------------- #
            handler_name = handler_identifier
            if handler_name in self.__active_handlers:
                handler = self.__active_handlers[handler_name]
                self.__logger.removeHandler(handler)
                handler.close()
                del self.__active_handlers[handler_name]
        
        elif isinstance(handler_identifier, Handler):
            # -- Remove by handler object ------------------------------------------- #
            handler_to_remove = handler_identifier
            handler_name_to_remove = None
            
            # -- Find the handler name by comparing handler objects –---------------- #
            for name, handler in self.__active_handlers.items():
                if handler is handler_to_remove:
                    handler_name_to_remove = name
                    break
            
            if handler_name_to_remove:
                self.__logger.removeHandler(handler_to_remove)
                handler_to_remove.close()
                del self.__active_handlers[handler_name_to_remove]
        
        else:
            raise TypeError("handler_identifier must be either a string (handler name) or a Handler object")

    def __create_file_handler(self, filepath: str, encoding: str = 'utf-8', mode: str = 'a') -> Handler:
        return logging.FileHandler(filename=filepath, encoding=encoding, mode=mode)

    def __ensure_path(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

    # ============================================================================
    #                              LOGGER METHODS
    # ============================================================================

    def init_term_handler(
        self,
        handler_name : str,
        level        : Optional[str] = 'info',
        fmt          : Optional[str] = '[%(levelname)s%(step)s] - %(message)s',
    ):
        handler = logging.StreamHandler(sys.stdout)
        
        self.modify_handler_level(handler, level)

        handler.setFormatter(
            ColorFormatter(fmt=fmt, datefmt=datefmt)
        )
        
        self.__add_handler( handler_name, handler )
    
    def init_file_handler(
        self,
        handler_name : str,
        path         : str,
        level        : Optional[str] = 'info',
        fmt          : Optional[str] = '[%(levelname)s%(step)s] - %(message)s',
        mode         : Optional[str] = 'w',
        encoding     : Optional[str] = 'utf-8'
    ) -> Handler:

        self.__ensure_path( path )

        # -- Configure a new file handler ------------------------------- #
        handler = self.__create_file_handler(path, mode=mode, encoding=encoding)
        self.modify_handler_level(handler, level)
        handler.setFormatter(
            logging.Formatter(fmt=fmt, datefmt=datefmt)
        )

        # -- Add the handler to the global logger ----------------------- #
        self.__add_handler(handler_name, handler)

        return handler

    def init_procedure_log_handler(
        self,
        handler_name    : str,
        path            : str,
        fmt             : Optional[str] = '%(step)s. %(message)s',  # Simple format for procedure log
        mode            : Optional[str] = 'w',
        encoding        : Optional[str] = 'utf-8'
    ) -> Handler:
        """Initialize a handler that only logs step and substep messages"""
        
        self.__ensure_path(path)
        
        # Create file handler
        handler = self.__create_file_handler(path, mode=mode, encoding=encoding)
        
        # Set level to capture both step and substep (use the lower level)
        self.modify_handler_level(handler, levels['step']['level'])
        
        # Add the step-only filter
        handler.addFilter( StepOnlyFilter() )
        
        # Set formatter (no timestamp/level needed for procedure log)
        handler.setFormatter( ProcedureFormater(fmt=fmt, datefmt=datefmt)  )
        
        # Add to logger
        self.__add_handler(handler_name, handler)
        
        return handler

    def remove_handler(
        self,
        handler_identifier : Union[str, Handler]
    ):
        self.__remove_handler(handler_identifier)

    def modify_handler_level(self, handler_identifier: Union[str, Handler], level: Union[str, int]) -> None:
        if isinstance(handler_identifier, Handler):
            handler_identifier.setLevel( self.__map_level(level) )
        
        elif isinstance(handler_identifier, str): 
            if handler_identifier in self.__active_handlers:
                self.__active_handlers[handler_identifier].setLevel( self.__map_level(level) )
                
        else:
            raise TypeError("handler_identifier must be either a string (handler name) or a Handler object")

        if self.__map_level(level) == get_level('debug'):
            self.__logger.setLevel( get_level('debug') )

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
        self.__ensure_path(path)

        # Open the file in write mode ('w')
        with open(path, 'w') as json_file:
            json.dump(self.__test_procedure, json_file, indent=4)


    # ============================================================================
    #                               LOGS METHODS
    # ============================================================================

    def debug(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = {"step": ""}

        if enable and args:
            msg = sep.join(str(a) for a in args) + end
            self.__logger.debug(msg, **kwargs, extra=extra)

    def info(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = {"step": ""}

        if enable and args: 
            msg = sep.join(str(a) for a in args) + end
            # Correctly call the logger.info method
            self.__logger.info(msg, **kwargs, extra=extra)

    def warning(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = {"step": ""}

        if enable and args:  
            msg = sep.join(str(a) for a in args) + end
            self.__logger.warning(msg, **kwargs, extra=extra)

    def error(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = {"step": ""}

        if enable and args:  
            msg = sep.join(str(a) for a in args) + end
            # Correctly call the logger.info method
            self.__logger.error(msg, **kwargs, extra=extra)

    def passed(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = {"step": ""}

        if enable and args: 
            msg = sep.join(str(a) for a in args) + end
            # Correctly call the logger.info method
            self.__logger._log(levels["pass"]["level"], msg, (), **kwargs, extra=extra)

    def fail(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = {"step": ""}

        if enable and args:
            msg = sep.join(str(a) for a in args) + end
            self.__logger._log(levels["fail"]["level"], msg, (), **kwargs, extra=extra)
    
    def step(self, *args, sep=' ', end='', enable=True, **kwargs):
        self.__stepn += 1
        self.__substepn = 0

        extra = {"step": f" {self.__stepn}"}

        if enable and args:  # Only log if enabled and there are arguments
            msg = sep.join(str(a) for a in args) + end
            # Correctly call the logger.info method
            self.__logger._log(levels["step"]["level"], msg, (), **kwargs, extra=extra)

        self.__test_procedure['steps'].append({
            'id': f"{self.__stepn}",
            'parent': None,
            'description': sep.join(str(a) for a in args) + end
        })

    def substep(self, *args, sep=' ', end='', enable=True, **kwargs):
        self.__substepn += 1

        extra = {"step": f" {self.__stepn}.{self.__substepn}"}

        if enable and args:  # Only log if enabled and there are arguments
            msg = sep.join(str(a) for a in args) + end
            self.__logger._log(levels["substep"]["level"], msg, (), **kwargs, extra=extra)

        self.__test_procedure['steps'].append({
            'id': f"{self.__stepn}.{self.__substepn}",
            'parent': f"{self.__stepn}",
            'description': sep.join(str(a) for a in args) + end
        }) 
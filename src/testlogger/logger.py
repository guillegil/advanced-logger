
from datetime import datetime
from functools import wraps
import json
import os
from logging import Logger, Handler

import logging
import shutil
from typing import Optional, Union

from colored import Fore as fg
from colored import Back as bg
from colored import Style as st

from pathlib import Path

datefmt = "%Y-%m-%d %H:%M:%S"

levels = {
    "debug"     : {"level": logging.DEBUG, "color": fg.CYAN},
    "info"      : {"level": logging.INFO, "color": fg.WHITE},
    "warning"   : {"level": logging.WARNING, "color": fg.YELLOW},
    "error"     : {"level": logging.ERROR, "color": fg.RED},
    "critical"  : {"level": logging.CRITICAL, "color": fg.RED},
    "step"      : {"level": 21, "color": fg.WHITE},
    "substep"   : {"level": 22, "color": fg.light_gray},
    "pass"      : {"level": 23, "color": fg.GREEN},
    "fail"      : {"level": 31, "color": fg.RED},
}

# -- Reverse lookup ------------------------------------------- #
levels_by_value = {v["level"]: k for k, v in levels.items()}


class ColorFormatter(logging.Formatter):

    RESET = st.RESET

    def __init__(self, fmt: str = None, datefmt: str = None, style='%'):
        if fmt is None:
            fmt = "[%(asctime)s] %(levelname)-8s %(message)s"

        # Register custom levels
        logging.addLevelName(levels['step']['level'], "STEP")
        logging.addLevelName(levels['substep']['level'], "SUBSTEP")
        logging.addLevelName(levels['pass']['level'], "PASS")
        logging.addLevelName(levels['fail']['level'], "FAIL")

        super().__init__(fmt, datefmt, style)

    def __get_level_by_value(self, target_level: int) -> tuple:
        key = levels_by_value.get(target_level)
        return (key, levels[key]) if key else (None, None)

    def format(self, record):
        # Get original formatted message
        formatted = super().format(record)

        # Get level info using reverse lookup
        level_key, level_info = self.__get_level_by_value(record.levelno)
        color = level_info["color"] if level_info else self.RESET

        # Add indentation for substep
        if level_key == "substep":
            formatted = "   " + formatted

        # Wrap the entire line in color, then reset
        return f"{color}{formatted}{self.RESET}"

class ProcedureFormater(logging.Formatter):

    def __init__(self, fmt: str = None, datefmt: str = None, style='%'):
        if fmt is None:
            fmt = "[%(asctime)s] %(levelname)-8s %(message)s"

        # Register custom levels
        logging.addLevelName(levels['step']['level'], "STEP")
        logging.addLevelName(levels['substep']['level'], "SUBSTEP")

        super().__init__(fmt, datefmt, style)

    def __get_level_by_value(self, target_level: int) -> tuple:
        key = levels_by_value.get(target_level)
        return (key, levels[key]) if key else (None, None)

    def format(self, record):
        # Get original formatted message
        formatted = super().format(record)

        # Get level info using reverse lookup
        level_key, level_info = self.__get_level_by_value(record.levelno)

        # Add indentation for substep
        if level_key == "substep":
            formatted = "   " + formatted

        # Wrap the entire line in color, then reset
        return formatted

class StepOnlyFilter(logging.Filter):
    """Filter that only allows step and substep log records through"""
    def filter(self, record):
        return record.levelno in [levels["step"]["level"], levels["substep"]["level"]]

class TestLogger:
    
    def __init__(
        self, 
        logger_name: str = "test_logger",
        *args,
        **kwargs
    ):
        self.__logger : Logger = logging.getLogger( logger_name )
        self.__logger.setLevel(levels['info']['level'])

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
    def logger(self) -> Logger:
        return self.__logger

    @property
    def test_procedure(self) -> dict:
        return self.__test_procedure

    @property
    def stepn(self) -> int:
        return self.__stepn

    # @stepn.setter
    # def stepn(self, step: int) -> None:
    #     self.__stepn = step

    @property
    def substepn(self) -> int:
        return self.__substepn

    # @substepn.setter
    # def substepn(self, substep: int) -> None:
    #     self.__substep = substep

    # ============================================================================
    #                              PRIVATE METHODS
    # ============================================================================

    def __map_level(self, level : Union[str, int]) -> int:
        if isinstance(level, str):
            clean_level = level.lower().replace(' ', '').replace('-', '').replace('_', '')
            return levels.get(clean_level, levels["info"])["level"]
        
        return level

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
        handler = logging.StreamHandler()
        
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

        if self.__map_level(level) == levels['debug']['level']:
            self.__logger.setLevel( levels['debug']['level'] )

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
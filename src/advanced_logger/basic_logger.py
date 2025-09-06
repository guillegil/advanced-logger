
from logging import Logger, Handler

import logging

import sys
from typing import Optional, Union

from .formatters import ColorFormatter, FileFormatter
from .levels import get_level_number, get_level
from .utils import *

datefmt = "%Y-%m-%d %H:%M:%S"

class BasicLogger:
    
    def __init__(
        self, 
        logger_name: str = "basic_logger_instance",
        *args,
        **kwargs
    ):
        self.__logger : Logger = logging.getLogger( logger_name )
        self.__logger.setLevel( self.INFO )

        self.__active_handlers: dict[str, Handler] = {}

        init_default_term_handler = kwargs.get('init_default_term_handler', False)

        if init_default_term_handler:
            self.init_term_handler('default_term_logger', level=self.INFO)
        
    @property
    def name(self) -> str:
        return self.logger.name
    
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

    @property
    def logger(self) -> Logger:
        return self.__logger

    @property
    def active_handlers(self) -> dict[str, Handler]:
        return self.__active_handlers

    # ============================================================================
    #                              PRIVATE METHODS
    # ============================================================================

    def _map_level(self, level : Union[str, int]) -> int:
        return get_level(level)

    def _add_handler(self, handler_name: str, handler: Handler) -> None:
        # -- Remove to avoid duplicates ------------------ #
        self._remove_handler(handler_name)

        self.__logger.addHandler( handler )
        self.__active_handlers[handler_name] = handler

    def _remove_handler(self, handler_identifier: Union[str, Handler]) -> None:
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

    def _create_file_handler(self, filepath: str, encoding: str = 'utf-8', mode: str = 'a') -> Handler:
        return logging.FileHandler(filename=filepath, encoding=encoding, mode=mode)

    # ============================================================================
    #                              LOGGER METHODS
    # ============================================================================

    def set_logger_level(self, level: int|str) -> None:
        level = get_level(level)
        
        self.logger.setLevel( level )

    def init_term_handler(
        self,
        handler_name : str,
        level        : Optional[str] = 'info',
        fmt          : Optional[str] = '[%(levelname)s] - %(message)s',
    ):
        handler = logging.StreamHandler(sys.stdout)
        
        self.set_handler_level(handler, level)

        handler.setFormatter(
            ColorFormatter(fmt=fmt, datefmt=datefmt)
        )
        
        self._add_handler( handler_name, handler )
    
    def init_file_handler(
        self,
        handler_name : str,
        path         : str,
        level        : Optional[str] = 'info',
        fmt          : Optional[str] = '[%(levelname)s] - %(message)s',
        mode         : Optional[str] = 'w',
        encoding     : Optional[str] = 'utf-8'
    ) -> Handler:

        ensure_path( path )

        # -- Configure a new file handler ------------------------------- #
        handler = self._create_file_handler(path, mode=mode, encoding=encoding)
        handler.setFormatter(
            FileFormatter(fmt=fmt, datefmt=datefmt)
        )

        self.set_handler_level(handler, level)

        # -- Add the handler to the global logger ----------------------- #
        self._add_handler(handler_name, handler)

        return handler

    def remove_handler(
        self,
        handler_identifier : Union[str, Handler]
    ):
        self._remove_handler(handler_identifier)

    def set_handler_level(self, handler_identifier: Union[str, Handler], level: Union[str, int]) -> None:
        level = get_level(level)
        
        if isinstance(handler_identifier, Handler):
            handler_identifier.setLevel( level )
        
        elif isinstance(handler_identifier, str): 
            if handler_identifier in self.__active_handlers:
                self.__active_handlers[handler_identifier].setLevel( level )
                
        else:
            raise TypeError("handler_identifier must be either a string (handler name) or a Handler object")

        if self._map_level(level) == get_level('debug'):
            self.__logger.setLevel( get_level('debug') )


    # ============================================================================
    #                               LOGS METHODS
    # ============================================================================

    def log(self, level: int, msg: str, extra=None, **kwargs):
        level = get_level_number(level)
        self.logger._log(level, msg, (), **kwargs, extra=extra)

    def debug(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = kwargs.pop('extra', {})

        if enable and args:
            msg = sep.join(str(a) for a in args) + end
            self.__logger.debug(msg, **kwargs, extra=extra)

    def info(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = kwargs.pop('extra', {})

        if enable and args: 
            msg = sep.join(str(a) for a in args) + end
            # Correctly call the logger.info method
            self.__logger.info(msg, **kwargs, extra=extra)

    def warning(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = kwargs.pop('extra', {})

        if enable and args:  
            msg = sep.join(str(a) for a in args) + end
            self.__logger.warning(msg, **kwargs, extra=extra)

    def error(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = kwargs.pop('extra', {})

        if enable and args:  
            msg = sep.join(str(a) for a in args) + end
            # Correctly call the logger.info method
            self.__logger.error(msg, **kwargs, extra=extra)

    def critical(self, *args, sep=' ', end='', enable=True, **kwargs):
        extra = kwargs.pop('extra', {})

        if enable and args:  
            msg = sep.join(str(a) for a in args) + end
            # Correctly call the logger.info method
            self.__logger.critical(msg, **kwargs, extra=extra)

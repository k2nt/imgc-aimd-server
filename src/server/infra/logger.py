from typing import List

from colorama import Fore, Back

import logging
import logging.config
from logging import Logger
from pathlib import Path


_DEFAULT_FORMAT = "%(asctime)s  %(levelname)s  %(message)s"
_DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# Format strings
_BOLD = '\033[1m'
_END = '\033[0m'


def white(*tp) -> str:
    """Returns a white-colored string."""
    t = ' '.join(tp)
    return Fore.WHITE + t + Fore.RESET

def cyan(*tp) -> str:
    """Returns a cyan-colored string."""
    t = ' '.join(tp)
    return Fore.LIGHTCYAN_EX + t + Fore.RESET

def magenta(*tp) -> str:
    """Returns a magenta-colored string."""
    t = ' '.join(tp)
    return Fore.LIGHTMAGENTA_EX + t + Fore.RESET

def cyan_bg(*tp) -> str:
    """Returns a string with cyan background."""
    t = ' '.join(tp)
    return Back.LIGHTCYAN_EX + t + Back.RESET

def red(*tp) -> str:
    """Returns a red-colored string."""
    t = ' '.join(tp)
    return Fore.RED + t + Fore.RESET

def red_bg(*tp) -> str:
    """Returns a string with red background and black foreground."""
    t = ' '.join(tp)
    return Back.RED + Fore.BLACK + t + Fore.RESET + Back.RESET

def green(*tp) -> str:
    """Returns a green-colored string."""
    t = ' '.join(tp)
    return Fore.LIGHTGREEN_EX + t + Fore.RESET

def green_bg(*tp) -> str:
    """Returns a string with green background and white foreground."""
    t = ' '.join(tp)
    return Back.LIGHTGREEN_EX + Fore.WHITE + t + Fore.RESET + Back.RESET

def yellow(*tp) -> str:
    """Returns a yellow-colored string."""
    t = ' '.join(tp)
    return Fore.LIGHTYELLOW_EX + t + Fore.RESET

def bold(*tp) -> str:
    """Returns a bolded string."""
    t = ' '.join(tp)
    return _BOLD + t + _END


def _color_by_log_level(s: str, level: int) -> str:
    match level:
        case logging.DEBUG:
            return cyan(s)
        case logging.INFO:
            return white(s)
        case logging.WARNING:
            return yellow(s)
        case logging.ERROR:
            return red(s)
        case logging.CRITICAL:
            return red(s)
        case _:
            return white(s)


class DefaultFormatter(logging.Formatter):
    """Custom formatter class for API logging."""
    def __init__(
            self, 
            fmt: str = _DEFAULT_FORMAT,
            datefmt: str = _DEFAULT_DATE_FORMAT,
    ):
        super().__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record: logging.LogRecord):                
        return _color_by_log_level(super().format(record), record.levelno)


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': DefaultFormatter,
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'MAIN': { 
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'uvicorn.error': { 
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('MAIN')

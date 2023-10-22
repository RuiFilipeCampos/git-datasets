""" logger.py - Extension and configuration of logger """

import logging
import logging.config

__all__ = ["get_logger"]


class ExtendedLogger(logging.Logger):
    """ Custom logger class with additional methods. """

    def console(self, msg, *args, **kwargs):
        """ Custom log level for console messages. """

        self.log(25, msg, *args, **kwargs)

class ColoredConsoleHandler(logging.StreamHandler):
    """Console handler with colored output."""
    
    COLORS = {
        'WARNING': '\033[93m',  # Yellow
        'INFO': '\033[94m',     # Blue
        'DEBUG': '\033[92m',    # Green
        'CRITICAL': '\033[91m', # Red
        'ERROR': '\033[91m',    # Red
        'DEFAULT': '\033[0m'    # Reset
    }

    def emit(self, record) -> None:
        # Change level name to title case (e.g., "ERROR" to "Error")
        record.levelname = record.levelname.title()
        color = self.COLORS.get(record.levelname.upper(), self.COLORS['DEFAULT'])
        msg = self.format(record)
        msg = msg.replace(record.levelname + ':', color + record.levelname + ':' + self.COLORS['DEFAULT'])
        self.stream.write(msg + '\n')
        self.stream.flush()


logging.setLoggerClass(ExtendedLogger)
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'colored_console': {
            '()': ColoredConsoleHandler,
            'formatter': 'default',
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['colored_console'],
        'level': 'DEBUG',
    }
})

def get_logger(name: str) -> ExtendedLogger:
    """Returns an instance of the ExtendedLogger for the specified name."""

    return logging.getLogger(name)

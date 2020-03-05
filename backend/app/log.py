import threading

import logging
import logging.config
from logging.handlers import RotatingFileHandler
from config import Config


class ThreadLogFilter(logging.Filter):
    """
    This filter only show log entries for specified thread name
    """

    def __init__(self, thread_name, *args, **kwargs):
        logging.Filter.__init__(self, *args, **kwargs)
        self.thread_name = thread_name

    def filter(self, record):
        return record.threadName == self.thread_name


def start_thread_logging():
    """
    Add a log handler to separate file for current thread
    """
    thread_name = threading.Thread.getName(threading.current_thread())
    log_file = '{}.log'.format(thread_name)

    log_handler = RotatingFileHandler(log_file, mode='a', maxBytes=5*1024*1024,
                                              backupCount=2, encoding=None, delay=0)

    log_handler.setLevel(Config.LOGGING_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)-15s"
        "| %(threadName)-11s"
        "| %(levelname)-5s"
        "| %(message)s")
    log_handler.setFormatter(formatter)

    log_filter = ThreadLogFilter(thread_name)
    log_handler.addFilter(log_filter)

    logger = logging.getLogger()
    logger.addHandler(log_handler)

    return log_handler


def stop_thread_logging(log_handler):
    # Remove thread log handler from root logger
    logging.getLogger().removeHandler(log_handler)

    # Close the thread log handler so that the lock on log file can be released
    log_handler.close()


# def worker():
#     thread_log_handler = start_thread_logging()
#     logging.info('Info log entry in sub thread.')
#     logging.debug('Debug log entry in sub thread.')
#     stop_thread_logging(thread_log_handler)


def config_root_logger():
    log_file = 'main.log'

    formatter = "%(asctime)-15s" \
                "| %(threadName)-11s" \
                "| %(levelname)-5s" \
                "| %(message)s"

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'root_formatter': {
                'format': formatter
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'root_formatter'
            },
            'log_file': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'filename': log_file,
                'formatter': 'root_formatter',
            }
        },
        'loggers': {
            '': {
                'handlers': [
                    'console',
                    # 'log_file',
                ],
                'level': 'DEBUG',
                'propagate': True
            }
        }
    })

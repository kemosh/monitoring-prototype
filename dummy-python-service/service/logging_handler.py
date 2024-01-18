import logging
import logging_loki
from sys import stdout

DEFAULT_LOG_FORMAT = "%(levelname)-8s %(asctime)s - PID:%(process)d - %(message)s"
DEFAULT_LOG_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

def get_logger(module_name):
    """
    To use this, do logger = get_logger(__name__)
    """
    logger = logging.getLogger(module_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def get_console_logger(module_name):
    # Define logger
    logger = logging.getLogger(module_name)

    # set logger level
    logger.setLevel(logging.DEBUG)

    # set formatter
    # logFormatter = logging.Formatter("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
    logFormatter = logging.Formatter(
        "%(asctime)s [%(name)12s] %(levelname)8s %(message)s"
    )

    # set streamhandler to stdout
    consoleHandler = logging.StreamHandler(stdout)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)
    return logger


def set_uvicorn_logger(
    log_format=DEFAULT_LOG_FORMAT, log_time_format=DEFAULT_LOG_TIME_FORMAT
):
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(log_format, log_time_format))
    logger.handlers.clear()
    logger.addHandler(handler)


def get_uvicorn_logger():
    return logging.getLogger("uvicorn.access")

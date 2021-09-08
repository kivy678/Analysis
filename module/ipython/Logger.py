# -*- coding:utf-8 -*-

__all__ = [
    "LOG"
]

#############################################################################

import os
import timeit

import logging
import logging.handlers

Path = os.path

#############################################################################

BASE_DIR        = Path.dirname(Path.realpath(__file__))
LOGGER_PATH     = Path.join(BASE_DIR, "dump")

LOGFMT_STRING   = "%(asctime)-15s|%(levelname)s|%(filename)s|%(lineno)d|%(module)s|%(funcName)s|%(message)s"
LOGFMT          = logging.Formatter(LOGFMT_STRING)

#############################################################################

def getLogger(name, LOG_FILE, stream=False):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    fileHandler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=32 * 1024 * 1024, backupCount=3
    )
    if stream:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(LOGFMT)
        logger.addHandler(streamHandler)

    fileHandler.setFormatter(LOGFMT)
    logger.addHandler(fileHandler)

    return logger


LOGGER_PATH = Path.join(LOGGER_PATH, "report")
LOG = getLogger("Report", LOGGER_PATH, False)

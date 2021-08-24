# -*- coding:utf-8 -*-

#############################################################################

import os
import timeit

import logging
import logging.handlers

from webConfig import LOGGER_PATH, LOG_PRINT

#############################################################################

__all__ = ["CODE_SPEED", "LOG"]

LOGFMT_STRING = "%(asctime)-15s|%(levelname)s|%(filename)s|%(lineno)d|%(module)s|%(funcName)s|%(message)s"
LOGFMT = logging.Formatter(LOGFMT_STRING)


class CODE_SPEED:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        start_time = timeit.default_timer()
        LOG.info("[*] START DOWNLOAD Time: " + str(start_time) + " *****")
        result = self.func(*args, **kwargs)
        LOG.info("***** WORKING END Time: "+ str(timeit.default_timer() - start_time)+ " *****")

        return True


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


LOGGER_PATH = os.path.join(LOGGER_PATH, "report")
LOG = getLogger("Report", LOGGER_PATH, LOG_PRINT)

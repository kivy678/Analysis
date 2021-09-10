# -*- coding:utf-8 -*-

__all__=[
    'getLogger'
]

##################################################################################################

import os

import logging
import logging.handlers

from kivy.clock import Clock

##################################################################################################


class MyLabelHandler(logging.Handler):

    def __init__(self, label, level=logging.NOTSET):
        logging.Handler.__init__(self, level=level)
        self.label = label
        self.event = None

    def emit(self, record):
        def f(dt=None):
            self.label.text += self.format(record)

        self.event = Clock.schedule_once(f)

    def __del__(self):
        if self.event:
            self.event.cancel()


def getLogger(name, label):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(MyLabelHandler(label, logging.INFO))

    return logger

# -*- coding:utf-8 -*-

__all__=[
    'getSession',
    'setSession',
    'popSession',
    'clearSession'
]

##################################################################################################

import os
from datetime import timedelta

from flask import session, escape
from flask_session import Session

from database.redisq import RedisQueue
from webConfig import REDIS_SESSION_CONFIG, FLASK_SESSION

##################################################################################################

rq = RedisQueue()
r_conn = rq.connect(REDIS_SESSION_CONFIG)

sess = Session()

##################################################################################################

def setup(app):
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=60)
    app.config['SESSION_FILE_THRESHOLD'] = 1000

    app.config['SESSION_USE_SIGNER'] = True
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SESSION_KEY_PREFIX'] = 'session'

    if r_conn:
        app.config['SESSION_TYPE'] = "redis"
        app.config['SESSION_REDIS'] = r_conn
    else:
        app.config['SESSION_TYPE'] = "filesystem"
        app.config['SESSION_FILE_DIR'] = FLASK_SESSION

    sess.init_app(app)

##################################################################################################

def getSession(k):
    return session.get(k, None)

def setSession(k, r):
    session[k] = r

def popSession(k):
    return session.pop(k, None)

def clearSession():
    session.clear()

##################################################################################################

# -*- coding:utf-8 -*-

#############################################################################

from flask import url_for

from app.session import getSession

#############################################################################

def getPkgName():
    if getSession('sha256') is None:
        return 'None'

    return getSession('pkgName')


def setup(app):
    app.jinja_env.globals.update(getPkgName=getPkgName)

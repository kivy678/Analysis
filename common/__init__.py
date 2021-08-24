# -*- coding:utf-8 -*-

from common.sharedpreference import SharedPreferences

def getSharedPreferences(fpath):
    return SharedPreferences(fpath)

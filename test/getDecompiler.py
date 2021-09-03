# -*- coding:utf-8 -*-

from module.android.AppManager.decompiler import *
from util.fsUtils import *

from common import getSharedPreferences
from webConfig import SHARED_PATH

sp                  = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR          = sp.getString('SAMPLE_DIR')

path = Join(SAMPLE_DIR, 'adware.apk')
#runJadx(path)
#runAndrog(path)
#runApktool(path)
#runApktool(path)

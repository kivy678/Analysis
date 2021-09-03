# -*- coding:utf-8 -*-

from module.android.AppManager.decompiler import *
from util.fsUtils import *

from common import getSharedPreferences
from webConfig import SHARED_PATH

sp                  = getSharedPreferences(SHARED_PATH)
DECODE_DIR          = sp.getString('DECODE_DIR')

path = Join(DECODE_DIR, '59A2A1F13BC065264B3DDA8FA76CC26BC182DB2BC1204205BBB162306FC66074', 'unzip')
#runJadx(path)
#runAndrog(path)
#runApktool(path)
#runApktool(path)
a = runIl2cpp(path, '59A2A1F13BC065264B3DDA8FA76CC26BC182DB2BC1204205BBB162306FC66074')
print(a)

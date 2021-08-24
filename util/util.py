# -*- coding:utf-8 -*-

################################################################################

import zipfile
from util.fsUtils import *

################################################################################

def zipDecompress(src, drc, pwd=None):
    DirCheck(drc)

    try:
        with zipfile.ZipFile(src) as zf:
            zf.extractall(drc, pwd=pwd)

        return True

    except Exception as e:
        print(e)
        return False

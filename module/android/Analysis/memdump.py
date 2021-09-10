# -*- coding:utf-8 -*-

##########################################################################

import subprocess as sub


from module.android.util.frida.dump.fridump3 import DUMP

from util.fsUtils import Join, DirCheck, Delete
from util.Logger import LOG

from common import getSharedPreferences
from webConfig import SHARED_PATH, BASE_DIR

##########################################################################

sp                  = getSharedPreferences(SHARED_PATH)
ANALYSIS_DIR        = sp.getString('ANALYSIS_DIR')

RUN_PATH            = Join(BASE_DIR, "module", "ipython", "getDumper.bat")

##########################################################################

def getMemoryDump(pkg):
    dump_path = Join(ANALYSIS_DIR, 'MEMORY', pkg)
    Delete(dump_path)
    DirCheck(dump_path)

    LOG.info(f"{'[*]':<5}START MEMORY DUMP")
    DUMP(dump_path, pkg, strings=True, log=False)
    LOG.info(f"{'[*]':<5}END MEMORY DUMP")

    return dump_path


def getPackerDump(pkg, pid):
    dump_path = Join(ANALYSIS_DIR, 'MEMORY', pkg)
    Delete(dump_path)
    DirCheck(dump_path)

    LOG.info(f"{'[*]':<5}START PACKER DUMP")
    sub.Popen(f"{RUN_PATH} {pid} {dump_path}").wait()
    LOG.info(f"{'[*]':<5}END PACKER DUMP")

    return dump_path

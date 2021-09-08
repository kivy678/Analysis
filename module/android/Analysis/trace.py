# -*- coding:utf-8 -*-

#############################################################################

from module.android.Analysis.process import ProcessInfor
from module.android.cmd import shell, adb

from util.fsUtils import Join
from util.Logger import LOG

from common import getSharedPreferences
from webConfig import SHARED_PATH

################################################################################

sp                  = getSharedPreferences(SHARED_PATH)
ANALYSIS_DIR        = sp.getString('ANALYSIS_DIR')
DUMP_PATH           = Join(ANALYSIS_DIR, 'strace.txt')

TRACE_TIMEOUT       = 60

################################################################################

def straceStart(pkg):
    LOG.info(f"{'[*]':<5}Start Strace")

    pif = ProcessInfor()
    pid = pif.getPid(pkg)

    if len(pid) < 1:
        LOG.info("Not Running Process")

    #cmd = f"strace -s 65535 -fF -t -i -x -o /data/local/tmp/strace.txt -p {int(pid[0])}"
    cmd = f"strace -s 65535 -t -i -x -o /data/local/tmp/strace.txt -p {int(pid[0])}"
    shell.runCommand(cmd, shell=True, timeout=TRACE_TIMEOUT)

    LOG.info("End Dump")

    LOG.info("Download DumpFile Start")
    cmd = f"adb pull /data/local/tmp/strace.txt {DUMP_PATH}"
    shell.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}End Strace")

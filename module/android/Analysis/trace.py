# -*- coding:utf-8 -*-

__all__=[
    'StraceManager'
]

#############################################################################

from threading import Thread

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

################################################################################

class StraceManager(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.pid = None
        self.pkg = None

    def run(self):
        self.straceStart()

    def setProcess(self, pkg):
        self.pkg = pkg
        pif = ProcessInfor()
        pid = pif.getPid(pkg)

        if pid is None:
            LOG.info(f"{'[*]':<5}Not Running Process")
            return False
        else:
            self.pid = int(pid[0])
            return True

    def straceStart(self):
        LOG.info(f"{'[*]':<5}Running stracing...")
        #cmd = f"strace -s 65535 -fF -t -i -x -o /data/local/tmp/strace.txt -p {int(pid[0])}"
        cmd = f"strace -s 65535 -t -i -x -o /data/local/tmp/strace.txt -p {self.pid}"
        shell.runCommand(cmd, shell=True)

    def straceStop(self):
        LOG.info(f"{'[*]':<5}End Strace & Dump")
        #cmd = f"kill -9 {self.pid}"
        cmd = f"am force-stop {self.pkg}"
        shell.runCommand(cmd, shell=True)

        LOG.info(f"{'[*]':<5}Download DumpFile Start")
        cmd = f"adb pull /data/local/tmp/strace.txt {DUMP_PATH}"
        shell.runCommand(cmd, shell=False)

        LOG.info(f"{'[*]':<5}End Strace")

        return DUMP_PATH

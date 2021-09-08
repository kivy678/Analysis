# -*- coding:utf-8 -*-

###########################################################################################

import re
from io import StringIO

from module.android.cmd import shell

from util.Logger import LOG

###########################################################################################


class ProcessInfor:
    def getPid(self, pkgName) -> list:
        #result = "'{print $2}'"
        #cmd = f"ps | grep {pkgName} | awk {result}"
        cmd = f"ps | grep {pkgName}"

        data = shell.runCommand(cmd, shell=True)
        if data == '':
            LOG.info(f"{'':>5}Not Running Process.")
            return None

        pid_list = [int(process.split()[1]) for process in data.split("\r\n")]
        return pid_list


    def getTPid(self, pid):
        cmd = f"cat /proc/{pid}/status"
        m = shell.runCommand(cmd, shell=True)

        r = re.compile(r".*^TracerPid:\s*(\d*)", re.M | re.S)
        with StringIO(m) as sio:
            tpid = r.match(sio.getvalue()).group(1)

        return tpid


    def getMaps(self, pid, mFilter=['']):
        cmd = f"cat /proc/{pid}/maps"
        m = shell.runCommand(cmd, shell=True)

        with StringIO(m) as sio, StringIO() as wio:
            for r in map(lambda s: re.compile(rf".*{s}.*", re.M)       \
                            .findall(sio.getvalue()), mFilter):
                for row in r:
                    wio.write(row)
                    wio.write('\n')

            return wio.getvalue()

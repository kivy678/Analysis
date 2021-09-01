# -*- coding:utf-8 -*-

###########################################################################################

from module.mobile.cmd import shell
from util.Logger import LOG

###########################################################################################

def setDebug(package, dbg=True):
    LOG.info(f"{'[*]':<5}Package Stop {package}")
    cmd = f"am force-stop {package}"
    shell.runCommand(cmd, shell=True)

    LOG.info(f"{'[*]':<5}Data Clear {package}")
    cmd = f"pm clear {package}"
    shell.runCommand(cmd, shell=True)

    mode = "set" if dbg else "clear"
    option = "-w" if dbg else ""

    cmd = f"am {mode}-debug-app {option} {package}"
    LOG.info(f"{'[*]':<5}am {mode}-debug-app {option} {package}")

    shell.runCommand(cmd, shell=True)

# -*- coding:utf-8 -*-

###########################################################################################

from module.mobile.cmd import shell

from util.fsUtils import PathSplit, Join
from util.Logger import LOG

###########################################################################################

def cmdInstall(_path):
    LOG.info(f"{'[*]':<5}start install: " + PathSplit(_path)[1])

    cmd = f"adb install -r {_path}"
    shell.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}Install End")

def cmdUninstall(pkg):
    LOG.info(f"{'[*]':<5}start uninstall: " + pkg)

    cmd = f"adb uninstall {pkg}"
    shell.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}uninstall End")


def cmdDownload(pkg, down):
    LOG.info(f"{'[*]':<5}start download: " + pkg)

    cmd = f"adb pull /data/app/{pkg}-1 {Join(down, pkg)}"
    shell.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}download End")

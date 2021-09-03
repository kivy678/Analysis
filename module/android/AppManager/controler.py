# -*- coding:utf-8 -*-

###########################################################################################

from util.fsUtils import *
from module.android.cmd import shell, adb
from module.android.AppManager.debug import debugger

from util.Logger import LOG

###########################################################################################

def appInstall(path):
    LOG.info(f"{'[*]':<5}start install: " + BaseName(path))
    adb.apkInstall(path)
    LOG.info(f"{'[*]':<5}Install End")

def appUninstall(pkg):
    LOG.info(f"{'[*]':<5}start uninstall: " + pkg)
    adb.apkUnInstall(pkg)
    LOG.info(f"{'[*]':<5}uninstall End")

def appDownload(pkg, path) -> str:
    LOG.info(f"{'[*]':<5}start download: " + pkg)
    return adb.apkDownload(pkg, path)
    LOG.info(f"{'[*]':<5}download End")

def appDebugger(path):
    LOG.info(f"{'[*]':<5}Endcode debugger Mode: " + BaseName(path))
    debugger(path)
    LOG.info(f"{'[*]':<5}Endcode debugger Mode: " + BaseName(path))

def appSetDebug(pkg, dbg=True):
    LOG.info(f"{'[*]':<5}set debug: " + pkg)
    adb.setDebug(pkg, dbg)
    LOG.info(f"{'[*]':<5}end debug: " + pkg)

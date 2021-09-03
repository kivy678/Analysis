# -*- coding:utf-8 -*-

#############################################################################

import re

from module.android.cmd import shell
from util.fsUtils import Join

#############################################################################

__all__ = [
    "adbDevices",
    "getDeviceList",
    "adbRestart",
    "apkInstall",
    "apkUnInstall",
    "apkDownload",
    "getModel",
    "getSystem",
    "getSdk",
    "getBootImage",
]

#############################################################################

def adbDevices():
    stdout = shell.runCommand("adb devices")
    return True if r'\n' in repr(stdout) else False

def getDeviceList():
    stdout = shell.runCommand("adb devices")
    dev_list = list(map(lambda x: re.match(r"(.*)\\t.*", x).group(1), repr(stdout).split(r'\r\n')[1:]))
    return dev_list

def adbRestart():
    shell.runCommand("adb kill-server")
    shell.runCommand("adb start-server")
    return True

#############################################################################

def apkInstall(path):
    shell.runCommand(f"adb install -r {path}")
    return True

def apkUnInstall(pkg):
    shell.runCommand(f"adb uninstall {pkg}")
    return True

def apkDownload(pkg, path):
    shell.runCommand(f"adb pull /data/app/{pkg}-1 {path}")
    return Join(path, 'base.apk')

#############################################################################

def setDebug(package, dbg):
    cmd = f"am force-stop {package}"
    shell.runCommand(cmd, shell=True)

    cmd = f"pm clear {package}"
    shell.runCommand(cmd, shell=True)

    mode = "set" if dbg else "clear"
    option = "-w" if dbg else ""

    cmd = f"am {mode}-debug-app {option} {package}"
    shell.runCommand(cmd, shell=True)

#############################################################################

def getModel(name):
    stdout = shell.runCommand("getprop ro.product.model", shell=True, name=name)
    return stdout

def getSystem(name):
    stdout = shell.runCommand("getprop ro.product.cpu.abi", shell=True, name=name)
    return stdout.replace('-', '_')

def getSdk(name):
    stdout = shell.runCommand("getprop ro.build.version.sdk", shell=True, name=name)
    return int(stdout)

def getBootImage(api, name):
    if api < 7:
        stdout = shell.runCommand("getprop ro.build.fingerprint", shell=True, name=name)
    else:
        stdout = shell.runCommand("getprop ro.bootimage.build.fingerprint", shell=True, name=name)

    return stdout


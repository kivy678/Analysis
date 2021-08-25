# -*- coding:utf-8 -*-

#############################################################################

from module.android.cmd import shell
import re

#############################################################################

__all__ = [
    "adbDevices",
    "adbRestart",
    "getModel",
    "getSystem",
    "getSdk",
    "getBootImage",
]

#############################################################################

def adbDevices():
    stdout = shell.runCommand("adb devices")
    #dev_list = list(map(lambda x: re.match(r"(.*)\\t.*", x).group(1), repr(stdout).split(r'\r\n')[1:]))
    #return dev_list
    return True if r'\n' in repr(stdout) else False

def adbRestart():
    shell.runCommand("adb kill-server")
    shell.runCommand("adb start-server")
    return None

#############################################################################

def getModel():
    stdout = shell.runCommand("getprop ro.product.model", shell=True)
    return stdout

def getSystem():
    stdout = shell.runCommand("getprop ro.product.cpu.abi", shell=True)
    return stdout.replace('-', '_')

def getSdk():
    stdout = shell.runCommand("getprop ro.build.version.sdk", shell=True)
    return int(stdout)

def getBootImage(api):
    if api < 7:
        stdout = shell.runCommand("getprop ro.build.fingerprint", shell=True)
    else:
        stdout = shell.runCommand("getprop ro.bootimage.build.fingerprint", shell=True)

    return stdout

# -*- coding:utf-8 -*-

#############################################################################

from module.android.cmd import shell
import re

#############################################################################

__all__ = [
    "adbDevices",
    "getDeviceList",
    "adbRestart",
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
    return None

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


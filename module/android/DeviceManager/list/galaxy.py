# -*- coding:utf-8 -*-

__all__=[
    "EMULATOR",
]

#############################################################################

from module.mobile.cmd import shell, adb
from module.mobile.DeviceManager.base import DEVICE_BASIS
from module.mobile.DeviceManager.install import DEVICE_INSTALLER

from util.fsUtils import SplitExt

#############################################################################

class EMULATOR(DEVICE_BASIS):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self._model = None
        self._installer = None

    def setup(self, dev_name=None):
        if self._isConnect:
            shell.runCommand("setenforce 0", shell=True)

            shell.runCommand("mount -o remount,rw /system", shell=True)
            shell.runCommand("mount -o remount,rw /", shell=True)

            self._model = adb.getModel()
            self._installer = DEVICE_INSTALLER(self.arch, self.sdk)

            return True

        else:
            return False

    @property
    def model(self):
        return self._model

    @property
    def installer(self):
        return self._installer


class GALAXY(DEVICE_BASIS):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def setup(self):
        shell.runCommand("adb root", shell=False)

        shell.runCommand("mount -o remount,rw /system", shell=True)
        shell.runCommand("mount -o remount,rw /", shell=True)


class LDPlayer(DEVICE_BASIS):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    @staticmethod
    def list():
        return list(map(lambda x: x.strip(), shell.runCommand("dnconsole list", shell=False).split()))

    @staticmethod
    def create(name=''):
        return shell.runCommand(f"dnconsole add --name {name}", shell=False)

    @staticmethod
    def remove(name):
        return shell.runCommand(f"dnconsole remove --name {name}", shell=False)

    @staticmethod
    def run(name):
        return shell.runCommand(f"dnconsole launch --name {name}", shell=False)

    @staticmethod
    def quit(name):
        return shell.runCommand(f"dnconsole quit --name {name}", shell=False)

    @staticmethod
    def reboot(name):
        return shell.runCommand(f"dnconsole reboot --name {name}", shell=False)

    @staticmethod
    def runApp(name, app):
        return shell.runCommand(f"dnconsole runapp --name {name} --packagename {app}", shell=False)

    @staticmethod
    def runKillApp(name, app):
        return shell.runCommand(f"dnconsole killapp --name {name} --packagename {app}", shell=False)

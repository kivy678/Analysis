# -*- coding:utf-8 -*-

__all__=[
    "GALAXY",
]

#############################################################################

from module.mobile.cmd import shell
from module.mobile.DeviceManager.base import DEVICE_BASIS

#############################################################################

class GALAXY(DEVICE_BASIS):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def setup(self):
        shell.runCommand("adb root", shell=False)

        shell.runCommand("mount -o remount,rw /system", shell=True)
        shell.runCommand("mount -o remount,rw /", shell=True)

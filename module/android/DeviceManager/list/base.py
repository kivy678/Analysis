# -*- coding:utf-8 -*-

#############################################################################

from module.android.cmd import shell, adb

#############################################################################


class DEVICE_BASIS:
    _ARCH_ = {
        "x86": "x86", "x64": "x64",
        "armeabi_v7a": "arm", "arm64_v8a": "arm64"
    }

    _isConnect  = None
    _arch       = None
    _model      = None
    _sdk        = None
    _su         = None

    def __init__(self, *args, **kwargs):
        self.name = kwargs['name']

        self._isConnect = adb.adbDevices()
        if self._isConnect:
            self._arch  = adb.getSystem(self.name)
            self._model = adb.getModel(self.name)
            self._sdk   = adb.getSdk(self.name)
            self._su    = self.isRoot(self.name)

    def __getattr__(self, key):
        try:
            return self._ARCH_[key]
        except KeyError as e:
            return None

    @classmethod
    def getPlatform(cls, **kwargs):
        return cls(**kwargs)

    @property
    def isConnect(self):
        return self._isConnect

    @property
    def model(self):
        return self._model

    @property
    def arch(self):
        return self._ARCH_[self._arch]

    @property
    def sdk(self):
        return self._sdk

    @property
    def su(self):
        return self._su

    def isRoot(self, name):
        stdout = shell.runCommand("if [ -f /system/bin/su ]; then echo True; fi", shell=True, name=name)
        if stdout == "":
            stdout = shell.runCommand("if [ -f /sbin/su ]; then echo True; fi", shell=True, name=name)

        if stdout == 'True':
            return True
        else:
            return False

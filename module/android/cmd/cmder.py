# -*- coding:utf-8 -*-

#############################################################################

from module.common.shell import SHELL
from functools import wraps

from common import getSharedPreferences
from webConfig import SHARED_PATH

#############################################################################

sp                  = getSharedPreferences(SHARED_PATH)
OS                  = sp.getString('OS')

#############################################################################

class COMMANDER(SHELL):
    def mode(f):
        @wraps(f)
        def inner(*args, **kwargs):
            self, cmd = args
            posix = False if OS == 'Windows' else True

            try:
                if kwargs['su'] is True:
                    cmd = repr('su -c ' + repr(cmd))
            except KeyError:
                pass

            try:
                if (kwargs['shell'] is True) and ('name' in kwargs):
                    cmd = f"adb -s {kwargs['name']} shell {cmd}"
                    posix = True

                elif kwargs['shell'] is True:
                    cmd = f"adb shell {cmd}"
                    posix = True

            except KeyError:
                pass

            try:
                if kwargs['java'] is True:
                    cmd = 'java -jar ' + cmd
            except KeyError:
                pass

            return f(self, cmd, posix, **kwargs)
        return inner

    @mode
    def runCommand(self, cmd, posix, shell=False, name=None, java=False, su=False, timeout=60, encoder='utf-8'):
        return super().runCommand(cmd, posix, timeout, encoder)

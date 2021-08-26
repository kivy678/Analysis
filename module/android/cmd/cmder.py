# -*- coding:utf-8 -*-

#############################################################################

from module.common.shell import SHELL
from functools import wraps

#############################################################################

class COMMANDER(SHELL):
    def mode(f):
        @wraps(f)
        def inner(*args, **kwargs):
            self, cmd = args

            try:
                if kwargs['su'] is True:
                    cmd = repr('su -c ' + repr(cmd))
            except KeyError:
                pass

            try:
                if (kwargs['shell'] is True) and (kwargs['name'] is not None):
                    cmd = f"adb -s {kwargs['name']} shell {cmd}"

            except KeyError:
                pass

            try:
                if kwargs['java'] is True:
                    cmd = 'java -jar ' + cmd
            except KeyError:
                pass

            return f(self, cmd, **kwargs)
        return inner

    @mode
    def runCommand(self, cmd, shell=False, name=None, java=False, su=False, timeout=60, encoder='utf-8'):
        return super().runCommand(cmd, timeout, encoder)

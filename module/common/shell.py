# -*- coding:utf-8 -*-

#############################################################################

import subprocess
import shlex

subp = subprocess.Popen

TIME_OUT = 60

#############################################################################

class SHELL(object):
    def runCommand(self, cmd, timeout=TIME_OUT, encoder='utf-8'):
        with subp(self.parseString(cmd), stdout=subprocess.PIPE) as proc:
            try:
                return proc.communicate(timeout=timeout)[0].decode(encoder).strip()
            except subprocess.TimeoutExpired:
                proc.kill()
                return proc.communicate()[0].decode(encoder).strip()
            except Exception as e:
                print(f"COMMAND ERROR: {cmd}: {e}")

    def parseString(self, cmd):
        s = shlex.shlex(cmd)
        s.whitespace_split = True

        return s

# -*- coding:utf-8 -*-

################################################################################

import glob

from module.android.cmd import shell

from util.util import zipDecompress
from util.fsUtils import *

from webConfig import SERVER_PATH, APP_PATH, TOOL_PATH, TOOL_USER_PATH

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.Logger import LOG

################################################################################

sp                  = getSharedPreferences(SHARED_PATH)
TMP_DIR             = sp.getString('TMP_DIR')

################################################################################

class DEVICE_INSTALLER():
    def __init__(self, cpu, sdk):
        self._cpu = cpu
        self._sdk = sdk

    def __del__(self):
        self.clean()

    def commit(self):
        cmd = f"mkdir /data/local/tmp/.cache"
        shell.runCommand(cmd, shell=True)

        cmd = f"echo '1' > /data/local/tmp/.cache/AndroidDevice"
        shell.runCommand(cmd, shell=True)

    def isCommit(self):
        cmd = f"find /data/local/tmp -type d -name .cache"
        stdout = shell.runCommand(cmd, shell=True)

        if stdout == '':
            return False
        else:
            cmd = f"find /data/local/tmp/.cache -name AndroidDevice"
            stdout = shell.runCommand(cmd, shell=True)

            return True if stdout != '' else False

    def appInstaller(self):
        LOG.info(f"{'':>5}[*] APP Install Start")

        for app in self.decompress(APP_PATH):
            cmd = f"adb install {app}"
            shell.runCommand(cmd, shell=False)

    def toolInstaller(self):
        for tool in self.decompress(TOOL_PATH): pass
        self.cowExploit()
        self.straceInstall()

    def serverInstaller(self):
        for tool in self.decompress(SERVER_PATH): pass
        self.fridaServer()
        self.androidServer()

    def userToolInstaller(self):
        if self._sdk >= 24:
            path = Join(TOOL_USER_PATH, 'api-24')
        elif self._sdk in [21, 22]:
            path = Join(TOOL_USER_PATH, 'api-22')

        for tool in self.decompress(path): pass
        self.userToolInstall()

    def cowExploit(self):
        LOG.info(f"{'':>5}[*] Cow Exploit Start")

        cmd = "adb push {0} /data/local/tmp".format(Join(TMP_DIR, 'mprop'))
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/mprop && cd /data/local/tmp && ./mprop ro.debuggable 1"
        shell.runCommand(cmd, shell=True)

        cmd = f"getprop ro.debuggable"
        shell.runCommand(cmd, shell=True)

    def straceInstall(self):
        LOG.info(f"{'':>5}[*] Strace Install Start")

        TOOL_PATH = Join(TMP_DIR, f"strace")

        cmd = f"adb push {TOOL_PATH} /system/strace"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /system/strace"
        shell.runCommand(cmd, shell=True)

        cmd = f"adb push {TOOL_PATH} /data/local/tmp/strace"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/strace"
        shell.runCommand(cmd, shell=True)

    def fridaServer(self):
        LOG.info(f"{'':>5}[*] frida-server Install Start")
        TOOL_PATH = Join(TMP_DIR, f"frida-server-12.7.15-android-{self._cpu}")

        cmd = f"adb push {TOOL_PATH} /system/frida-server"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /system/frida-server"
        shell.runCommand(cmd, shell=True)

        #cmd = f"nohup /system/frida-server"
        #shell.runCommand(cmd, shell=True, su=True)

        cmd = f"adb push {TOOL_PATH} /data/local/tmp/frida-server"
        shell.runCommand(cmd, shell=False)

        LOG.info(f"{'':>5}[*] frida-server Run")
        cmd = f"chmod 755 /data/local/tmp/frida-server"
        shell.runCommand(cmd, shell=True)

        #cmd = f"nohup /data/local/tmp/frida-server"
        #shell.runCommand(cmd, shell=True, su=True)

    def androidServer(self):
        LOG.info(f"{'':>5}[*] android-server Install Start")
        TOOL_PATH = Join(TMP_DIR, f"android_{self._cpu}_server")

        cmd = f"adb forward tcp:22222 tcp:22222"
        shell.runCommand(cmd, shell=False)

        cmd = f"adb push {TOOL_PATH} /data/local/tmp/android_server"
        shell.runCommand(cmd, shell=False)

        LOG.info(f"{'':>5}[*] android-server Run")
        cmd = f"chmod 755 /data/local/tmp/android_server"
        shell.runCommand(cmd, shell=True)

        #cmd = f"nohup /data/local/tmp/android_server"
        #shell.runCommand(cmd, shell=True, su=True)

    def userToolInstall(self):
        LOG.info(f"{'':>5}[*] User-Tool Install Start")

        TOOL_PATH = Join(TMP_DIR, f"GetMemory_{self._cpu}")

        cmd = f"adb push {TOOL_PATH} /data/local/tmp/GetMemory"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/GetMemory"
        shell.runCommand(cmd, shell=True)

        TOOL_PATH = Join(TMP_DIR, f"ReadMemory_{self._cpu}")

        cmd = f"adb push {TOOL_PATH} /data/local/tmp/ReadMemory"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/ReadMemory"
        shell.runCommand(cmd, shell=True)

        TOOL_PATH = Join(TMP_DIR, f"WriteMemory_{self._cpu}")

        cmd = f"adb push {TOOL_PATH} /data/local/tmp/WriteMemory"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/WriteMemory"
        shell.runCommand(cmd, shell=True)

        TOOL_PATH = Join(TMP_DIR, f"SearchMemory_{self._cpu}")

        cmd = f"adb push {TOOL_PATH} /data/local/tmp/SearchMemory"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/SearchMemory"
        shell.runCommand(cmd, shell=True)

        TOOL_PATH = Join(TMP_DIR, f"trace_{self._cpu}")

        cmd = f"adb push {TOOL_PATH} /data/local/tmp/trace"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/trace"
        shell.runCommand(cmd, shell=True)

    def decompress(self, d_path):
        for _path in glob.glob(Join(d_path, '*')):
            zipDecompress(_path, TMP_DIR)

            yield Join(TMP_DIR, BaseName(_path).replace('zip', 'apk'))

    def clean(self):
        Delete(TMP_DIR)
        DirCheck(TMP_DIR)

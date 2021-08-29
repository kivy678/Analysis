# -*- coding:utf-8 -*-

################################################################################

import glob

from module.mobile.cmd import shell

from util.util import zipDecompress
from util.fsUtils import *

from webConfig import SERVER_PATH, APP_PATH, TOOL_PATH, TOOL_USER_PATH

from common import getSharedPreferences
from webConfig import SHARED_PATH

################################################################################

sp                  = getSharedPreferences(SHARED_PATH)
TMP_DIR             = sp.getString('TMP_DIR')

################################################################################

class DEVICE_INSTALLER():
    def __init__(self, cpu, sdk):
        self._cpu = cpu
        self._sdk = sdk
        self.clean()

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


    def toolInstall(self):
        TOOL_PATH = Join(TMP_DIR, f"strace")

        cmd = f"adb push {TOOL_PATH} /system/strace"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /system/strace"
        shell.runCommand(cmd, shell=True)

        cmd = f"adb push {TOOL_PATH} /data/local/tmp/strace"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/strace"
        shell.runCommand(cmd, shell=True)



    def userToolInstall(self):
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



    def fridaServer(self):
        TOOL_PATH = Join(
            TMP_DIR, f"frida-server-12.7.15-android-{self._cpu}")
        cmd = f"adb push {TOOL_PATH} /system/frida-server"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /system/frida-server"
        shell.runCommand(cmd, shell=True)

        #cmd = f"nohup /system/frida-server"
        #shell.runCommand(cmd, shell=True, su=True)

        cmd = f"adb push {TOOL_PATH} /data/local/tmp/frida-server"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/frida-server"
        shell.runCommand(cmd, shell=True)

        #cmd = f"nohup /data/local/tmp/frida-server"
        #shell.runCommand(cmd, shell=True, su=True)


    def androidServer(self):
        TOOL_PATH = Join(TMP_DIR, f"android_{self._cpu}_server")

        cmd = f"adb forward tcp:22222 tcp:22222"
        shell.runCommand(cmd, shell=False)

        cmd = f"adb push {TOOL_PATH} /data/local/tmp/android_server"
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/android_server"
        shell.runCommand(cmd, shell=True)

        #cmd = f"nohup /data/local/tmp/android_server"
        #shell.runCommand(cmd, shell=True, su=True)


    def cowExploit(self):
        cmd = "adb push {0} /data/local/tmp".format(Join(TMP_DIR, 'mprop'))
        shell.runCommand(cmd, shell=False)

        cmd = f"chmod 755 /data/local/tmp/mprop && cd /data/local/tmp && ./mprop ro.debuggable 1"
        shell.runCommand(cmd, shell=True)

        cmd = f"getprop ro.debuggable"
        shell.runCommand(cmd, shell=True)


    def appInstaller(self):
        for app in self.appDecompress():
            cmd = f"adb install {app}"
            shell.runCommand(cmd, shell=False)


    def appDecompress(self):
        for _path in glob.glob(Join(APP_PATH, '*')):
            _, app_name = PathSplit(_path)

            zipDecompress(_path, TMP_DIR)

            yield Join(TMP_DIR, app_name.replace('zip', 'apk'))


    def serverDecompress(self):
        for _path in glob.glob(Join(SERVER_PATH, '*')):
            _, server_name = PathSplit(_path)

            zipDecompress(_path, TMP_DIR)


    def toolDecompress(self):
        for _path in glob.glob(Join(TOOL_PATH, '*')):
            _, server_name = PathSplit(_path)

            zipDecompress(_path, TMP_DIR)


    def userToolDecompress(self):
        if self._sdk >= 24:
            path = Join(TOOL_USER_PATH, 'api-24')
        elif self._sdk in [21, 22]:
            path = Join(TOOL_USER_PATH, 'api-22')

        for _path in glob.glob(Join(path, '*')):
            _, server_name = PathSplit(_path)

            zipDecompress(_path, TMP_DIR)


    def clean(self):
        Delete(TMP_DIR)
        DirCheck(TMP_DIR)

# -*- coding:utf-8 -*-

#############################################################################
__all__=[
    "dynamicServer",
]
#############################################################################

import time
from multiprocessing import Process

from module.android.cmd import shell, adb
from util.Logger import LOG

#############################################################################

def jdbStart():
    LOG.info(f"{'[*]':<5}Start jdb")

    _port = shell.runCommand(f"adb jdwp", shell=False)
    for port in _port.split():
        LOG.info(f"{'[*]':<5}jdwp number: {port}")

        shell.runCommand(f"adb forward tcp:23947 jdwp:{port}", shell=False)
        shell.runCommand(f"jdb -connect com.sun.jdi.SocketAttach:hostname=localhost,port=23947", shell=False)

    LOG.info(f"{'[*]':<5}jdwp END")

def startFridaServer():
    LOG.info(f"{'':>5}[*] frida-server Run")

    cmd = f"cd /system && ./frida-server"
    shell.runCommand(cmd, shell=True, su=True)

    #cmd = f"cd /data/local/tmp && ./frida-server"
    #shell.runCommand(cmd, shell=True, su=True)

def startAndroidServer():
    LOG.info(f"{'':>5}[*] android-server Run")

    cmd = f"adb forward tcp:22222 tcp:22222"
    shell.runCommand(cmd, shell=False)

    cmd = f"cd /data/local/tmp && ./android_server -p22222"
    shell.runCommand(cmd, shell=True, su=True)

def dynamicServer():
    LOG.info(f"{'[*]':<5}Start Server")

    for server in [startFridaServer, startAndroidServer]:
        s = Process(target=server)
        s.start()
        time.sleep(5)

        s.terminate()
        while s.is_alive():
            time.sleep(1)

        s.close()

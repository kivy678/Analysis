# -*- coding:utf-8 -*-

###########################################################################################

import os
import sys

import frida

from util.fsUtils import Join
from util.Logger import LOG

###########################################################################################

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
JS_PATH = Join(BASE_DIR, "js", "merge.js")

###########################################################################################

def on_message(message, data):
    if message["type"] == "send":
        print(message["payload"])
    else:
        print(message)


def Hook(_PACKAGE_NAME):
    with open(JS_PATH, 'r') as fr:
        jscode = fr.read()

    try:
        device = frida.get_usb_device(timeout=10)
        pid = device.spawn([_PACKAGE_NAME])
        LOG.info(f"App is starting ... pid : {pid}")

        process = device.attach(pid)
        device.resume(pid)

        script = process.create_script(jscode)
        script.on('message', on_message)
        LOG.info('[*] Running Hooking App')
        script.load()
        sys.stdin.read()

    except Exception as e:
        LOG.info(e)
        LOG.info("Exception END...")

    LOG.info("[*] End Hooking App")


def attachHook(_PACKAGE_NAME):
    with open(JS_PATH, 'r') as fr:
        jscode = fr.read()

    try:
        device = frida.get_usb_device(timeout=10)
        process = device.attach(_PACKAGE_NAME)
        LOG.info(f"App is Attaching ... pid : {process}")

        script = process.create_script(jscode)
        script.on('message', on_message)
        LOG.info('[*] Running Hooking App')
        script.load()
        sys.stdin.read()

    except Exception as e:
        LOG.info(e)
        LOG.info("Exception END...")

    LOG.info("[*] End Hooking App")

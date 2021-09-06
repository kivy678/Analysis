# -*- coding:utf-8 -*-

__all__=[
    'runJadx',
    'runAndrog',
    'runUnzip',
    'runApktool',
    'runMono',
    'runIl2cpp'
]

###########################################################################################

from module.android.AppManager.unity import runDecodeMono, runDecodeil2cpp
from module.android.cmd import shell
from util.Logger import LOG

from common import getSharedPreferences
from webConfig import SHARED_PATH, DECOMPLIE_PATH

from util.fsUtils import *
from util.util import zipDecompress

###########################################################################################

sp                  = getSharedPreferences(SHARED_PATH)

SAMPLE_DIR          = sp.getString('SAMPLE_DIR')
DECODE_DIR          = sp.getString('DECODE_DIR')
TMP_DIR             = sp.getString('TMP_DIR')

APK_TOOL            = Join(DECOMPLIE_PATH, "apktool_2.4.1.jar")
JADXpath            = sp.getString('JADXpath')

###########################################################################################

def runJadx(path) -> str:
    _, fileName = PathSplit(path)

    dst = Join(DECODE_DIR, fileName, 'jadx')
    DirCheck(dst)

    LOG.info(f"{'[*]':<5}Start JADX Decode: {fileName}")

    cmd = f"{JADXpath} -r -d {dst} {path}"
    shell.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}End Decode")

    return dst


def runAndrog(path) -> str:
    _, fileName = PathSplit(path)
    dst = Join(DECODE_DIR, fileName, 'androg')
    DirCheck(dst)

    LOG.info(f"{'[*]':<5}Start Androg Decode: {fileName}")

    cmd = f"androguard decompile -o {dst} {path}"
    shell.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}End Decode")

    return dst


def runUnzip(path) -> str:
    _, fileName = PathSplit(path)
    dst = Join(DECODE_DIR, fileName, 'unzip')
    DirCheck(dst)

    LOG.info(f"{'[*]':<5}Start unzip: {fileName}")
    zipDecompress(path, dst)

    LOG.info(f"{'[*]':<5}End decode: {fileName}")

    return dst


def runApktool(path) -> str:
    _, fileName = PathSplit(path)
    dst = Join(DECODE_DIR, fileName, 'apktool')
    DirCheck(dst)

    LOG.info(f"{'[*]':<5}Start apktool: {fileName}")
    cmd = f"{APK_TOOL} d -f -o {dst} {path}"
    shell.runCommand(cmd, java=True)

    LOG.info(f"{'[*]':<5}End apktool: {fileName}")

    return dst


def runMono(path, fileName) -> str:
    dst = Join(DECODE_DIR, fileName, 'mono')
    DirCheck(dst)

    LOG.info(f"{'[*]':<5}Start mono: {fileName}")
    runDecodeMono(path, fileName)

    LOG.info(f"{'[*]':<5}End mono: {fileName}")

    return dst


def runIl2cpp(path, fileName) -> str:
    dst = Join(DECODE_DIR, fileName, 'il2cpp')
    DirCheck(dst)

    LOG.info(f"{'[*]':<5}Start il2cpp: {fileName}")
    runDecodeil2cpp(path, fileName)

    LOG.info(f"{'[*]':<5}End il2cpp: {fileName}")

    return dst

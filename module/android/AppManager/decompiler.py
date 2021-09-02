# -*- coding:utf-8 -*-

__all__=[
    'runJadx',
    'runAndrog',
    'runUnzip',
    'runApktool',

]

###########################################################################################

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
JADX_PATH = sp.getString('JADX_PATH')

###########################################################################################

def runJadx(_path) -> str:
    _, fileName = PathSplit(_path)

    dst = Join(DECODE_DIR, fileName, 'jadx')
    DirCheck(dst)

    LOG.info(f"{'[*]':<5}Start JADX Decode: {fileName}")

    cmd = f"{JADX_PATH} -r -d {dst} {_path}"
    shell.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}End Decode")

    return dst


def runAndrog(_path) -> str:
    _, fileName = PathSplit(_path)
    dst = Join(DECODE_DIR, fileName, 'androg')
    DirCheck(dst)

    LOG.info(f"{'[*]':<5}Start Androg Decode: {fileName}")

    cmd = f"androguard decompile -o {dst} {_path}"
    shell.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}End Decode")

    return dst


def runUnzip(_path) -> str:
    _, fileName = PathSplit(_path)
    dst = Join(DECODE_DIR, fileName, 'unzip')
    DirCheck(dst)

    LOG.info(f"{'[*]':<5}start unzip: {fileName}")
    zipDecompress(_path, dst)

    LOG.info(f"{'[*]':<5}End decode: {fileName}")

    return dst


def runApktool(_path) -> str:
    _, fileName = PathSplit(_path)
    dst = Join(DECODE_DIR, fileName, 'apktool')
    DirCheck(dst)

    LOG.info(f"{'[*]':<5}start apktool: {fileName}")
    cmd = f"{APK_TOOL} d -f -o {dst} {_path}"
    shell.runCommand(cmd, java=True)

    LOG.info(f"{'[*]':<5}start apktool: {fileName}")

    return dst

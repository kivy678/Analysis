# -*- coding:utf-8 -*-

__all__=[
    'debugger'
]

###########################################################################################

import os
from bs4 import BeautifulSoup

from module.mobile.cmd import shell

from util.fsUtils import *
from util.Logger import LOG

from webConfig import *

from common import getSharedPreferences
from webConfig import SHARED_PATH

###########################################################################################

sp                  = getSharedPreferences(SHARED_PATH)
TMP_DIR             = sp.getString('TMP_DIR')

APK_TOOL            = Join(DECOMPLIE_PATH,  "apktool_2.4.1.jar")

SIGNAPK_TOOL        = Join(DECOMPLIE_PATH,  "signapk", "signapk.jar")
CERTIFICATE_TOOL    = Join(DECOMPLIE_PATH,  "signapk", "certificate.pem")
PK8_TOOL            = Join(DECOMPLIE_PATH,  "signapk", "key.pk8")

DBG_DIR             = Join(TMP_DIR,         "dbg")
DECODE_PATH         = Join(DBG_DIR,         "decode")

MANIFEST            = Join(DECODE_PATH,     "AndroidManifest.xml")
MANIFEST_WRITE      = Join(DECODE_PATH,     "AndroidManifest_tmp.xml")

OUT_APK             = Join(DBG_DIR,         "out.apk")
KEY_APK             = Join(DBG_DIR,         "signed.apk")

###########################################################################################

def cleanDir():
    for path in [DBG_DIR]:
        Delete(path)
        DirCheck(path)

def readManifest():
    try:
        with open(MANIFEST, "r", encoding='utf-8') as fr:
            soup = BeautifulSoup(fr, "lxml-xml")
            soup.application['android:debuggable'] = 'true'

            with open(MANIFEST_WRITE, "w", encoding='utf-8') as fw:
                fw.write(str(soup))
    except Exception as e:
        LOG.info(e)
        exit()


def fileManger():
    try:
        Delete(MANIFEST)
        os.rename(MANIFEST_WRITE, MANIFEST)
    except Exception as e:
        LOG.info(e)
        return False


def debugger(_path, force=False):
    option = '-f' if force else ''
    cleanDir()

    fdir, fileName = PathSplit(_path)
    tmp_dst = Join(TMP_DIR, fileName)

    Copy(_path, tmp_dst)

    LOG.info(f"{'[*]':<5}start decode: {fileName}")

    cmd = f"{APK_TOOL} d {option} -o {DECODE_PATH} {tmp_dst}"
    shell.runCommand(cmd, java=True)

    #readManifest()
    #fileManger()

    LOG.info(f"{'[*]':<5}start build")
    cmd = f"{APK_TOOL} b {option} -d -o {OUT_APK} {DECODE_PATH}"
    shell.runCommand(cmd, java=True)

    LOG.info(f"{'[*]':<5}sign code")
    cmd = f"{SIGNAPK_TOOL} {CERTIFICATE_TOOL} {PK8_TOOL} {OUT_APK} {KEY_APK}"
    shell.runCommand(cmd, java=True)

    f, ext = SplitExt(fileName)
    signed_apk = Join(fdir, f+'_signed.apk')
    Copy(KEY_APK, signed_apk)

    LOG.info(f"{'[*]':<5}File Clean")
    cleanDir()

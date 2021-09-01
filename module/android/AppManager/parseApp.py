# -*- coding:utf-8 -*-

__all__=[
    'setApplicationInfor'
]

###########################################################################################

import glob

from module.mobile.cmd import shell

from module.mobile.AppManager.app import APP_INFOR

from util.Logger import LOG
from util.parser import *
from util.fsUtils import *
from util.util import zipDecompress
from util.hash import getSHA256

from webConfig import *

from common import getSharedPreferences
from webConfig import SHARED_PATH

###########################################################################################

sp                  = getSharedPreferences(SHARED_PATH)

SAMPLE_DIR          = sp.getString('SAMPLE_DIR')
DECODE_DIR          = sp.getString('DECODE_DIR')
TMP_DIR             = sp.getString('TMP_DIR')

APK_TOOL 			= Join(DECOMPLIE_PATH, "apktool_2.4.1.jar")

###########################################################################################

def cleanDir():
    for path in [TMP_DIR]:
        Delete(path)
        DirCheck(path)

def readySample(_path) -> str: 			# DecodePath
    _, fileName = PathSplit(_path)
    tmp_dst = Join(TMP_DIR, fileName)

    Copy(_path, tmp_dst)

    LOG.info(f"{'[*]':<5}start unzip: {fileName}")
    zipDecompress(tmp_dst, Join(DECODE_DIR, fileName, 'unzip'))

    LOG.info(f"{'[*]':<5}start decode: {fileName}")

    DECODE_PATH = Join(DECODE_DIR, fileName, 'apktool')
    cmd = f"{APK_TOOL} d -f -o {DECODE_PATH} {_path}"
    shell.runCommand(cmd, java=True)

    return DECODE_PATH


def setApplicationInfor(_path):
    _, fileName = PathSplit(_path)
    app = APP_INFOR()

    app.decodePath = readySample(_path)
    app.sha256 = getSHA256(_path)
    app.fileName = fileName

    MANIFEST = Join(app.decodePath, "AndroidManifest.xml")

    LOG.info(f"{'':>5}Start XML Parsing")
    app.parser(XmlParser(MANIFEST))

    LOG.info(f"{'':>5}Start JSON Parsing")
    app.parser(JsonParser(MANIFEST))

    LOG.info(f"{'[*]':<5}PackageName:{app.pkgName}")
    cleanDir()

    return (app.pkgName, app.fileName)

# -*- coding:utf-8 -*-

###########################################################################################

from module.mobile.cmd import shell
from util.Logger import LOG

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.fsUtils import Join, PathSplit, DirCheck

###########################################################################################

sp = getSharedPreferences(SHARED_PATH)
DECODE_DIR = sp.getString('DECODE_DIR')

###########################################################################################

def runAndrogDecode(_path):
    _, fileName = PathSplit(_path)
    dst = Join(DECODE_DIR, fileName, 'androg')
    DirCheck(dst)

    LOG.info(f"{'[*]':<5}Start Androg Decode: {fileName}")

    cmd = f"androguard decompile -o {dst} {_path}"
    shell.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}End Decode")

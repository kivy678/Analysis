# -*- coding:utf-8 -*-

###########################################################################################

from module.mobile.cmd import shell
from util.Logger import LOG

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.fsUtils import Join, PathSplit, DirCheck

###########################################################################################

sp = getSharedPreferences(SHARED_PATH)
JADX_PATH = sp.getString('JADX_PATH')
DECODE_DIR = sp.getString('DECODE_DIR')

###########################################################################################

def runJadxDecode(_path):
    _, fileName = PathSplit(_path)
    dst = Join(DECODE_DIR, fileName, 'jadx')
    DirCheck(dst)

    LOG.info(f"{'[*]':<5}Start JADX Decode: {fileName}")

    cmd = f"{JADX_PATH} -r -d {dst} {_path}"
    shell.runCommand(cmd, shell=False)

    LOG.info(f"{'[*]':<5}End Decode")

# -*- encoding: utf-8 -*-

#############################################################################

from hurry.filesize import size as convSize
from hurry.filesize import alternative

from util.fsUtils import *

from common import getSharedPreferences
from webConfig import SHARED_PATH

import disassemble

################################################################################

sp                  = getSharedPreferences(SHARED_PATH)
DECODE_DIR          = sp.getString('DECODE_DIR')
DATA_DIR            = sp.getString("DATA_DIR")

################################################################################

def findFile(dir, fileName):
    for _path in Walk(dir):
        if PathSplit(_path)[1] == fileName:
            return _path

def fetch_disasm(arch, text):
    opcode = ''.join([f"\\x{opcode}" for opcode in text.split()]).encode()
    opcode = opcode.decode('unicode-escape').encode('ISO-8859-1')

    return getattr(disassemble, f'disasm{arch}')(opcode)


def lib_List(sha256):
    data = list()

    if sha256 is None:
        return []

    analysis_path = Join(DECODE_DIR, sha256, 'unzip')

    for path in Walk(analysis_path):
        p = BaseName(path)

        if SplitExt(p)[1] == ".so":
            data.append(path)

    data = map(lambda x: x.replace(analysis_path, '')[1:], data)
    return data

def ida_List(sha256):
    data = list()

    if sha256 is None:
        return []

    analysis_path = Join(DECODE_DIR, sha256, 'unzip')

    for _path in Walk(analysis_path):
        p = PathSplit(_path)[1]
        ext = SplitExt(p)[1]

        if p == "libil2cpp.so":
            continue
        elif ext == ".so":
            data.append(_path)

    data = map(lambda x: (x.replace(analysis_path, '')[1:], convSize(FileSize(x), system=alternative)), data)
    return data

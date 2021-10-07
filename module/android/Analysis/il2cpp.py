# -*- coding:utf-8 -*-

################################################################################

import os
import re

import struct

from io import StringIO

from util.fsUtils import *
from util.hash import *
from util.parser import JSON

from util.Logger import LOG

################################################################################

class ESCAPE_CONDITION(Exception):
    pass

STRIP_HEX = [r'0xE3A0..00', r'0xE12FFF1E', r'0xE320F000']
DETECTED_HEX = [r'0xE320F000',                  # NOP
                r'0xE3A00000 0xE12FFF1E',       # mov R0, #0; BX LR                 00 00 a0 e3 1e ff 2f e1
                r'0xE0400000 0xE12FFF3E',       # sub r0, r0, r0; BLX LR            00 00 40 e0 3e ff 2f e1
                r'0xE3E00102 0xE12FFF1E',       # mov R0, #0x7FFFFFFF; BX LR        02 01 e0 e3 1e ff 2f e1
                r'0xE3E004FF 0xE12FFF1E',       # MOV R0, #0xFFFFFF; BLX LR         ff 04 e0 e3 1e ff 2f e1
                r'0xFEDEFFE7',                  # TRAP
]

ORG_COMILE_HEX = [re.compile(x) for x in STRIP_HEX]

IL2CPP_FILE         = "libil2cpp.so"

################################################################################

def searchFile(dir, fileName):
    for i in Walk(dir):
        if PathSplit(i)[1] == fileName:
            return i

def isSizeSame(opath, hpath):
    return True if GetSize(opath) == GetSize(hpath) else False

def getULong(fr):
    content = fr.read(4)
    return struct.unpack("<L", content)[0] if content else None

def longToHex(v):
    return '0x{:X}'.format(v)


def startCmp(CMP1, CMP2):
    CMP1 = searchFile(Join(CMP1, 'lib'), IL2CPP_FILE)
    CMP2 = searchFile(Join(CMP2, 'lib'), IL2CPP_FILE)

    if not isSizeSame(CMP1, CMP2):
        return (False, "IL2CPP 사이즈가 다릅니다.")


    f_cmp1       = open(CMP1, 'rb')
    f_cmp2       = open(CMP2, 'rb')

    Json_Buffer  = StringIO()

    while True:
        bin_cmp1 = getULong(f_cmp1)
        bin_cmp2 = getULong(f_cmp2)

        if (bin_cmp1 is None) or (bin_cmp2 is None):
            break

        try:
            if bin_cmp1 != bin_cmp2:
                for p in ORG_COMILE_HEX:
                    if p.match(longToHex(bin_cmp2)):
                        raise ESCAPE_CONDITION(longToHex(bin_cmp2))

                json_encoder = {"offset": f_cmp1.tell()-4, "CMP1_BIN": bin_cmp2, "CMP2_BIN": bin_cmp1}
                JSON.dump(json_encoder, Json_Buffer)
                Json_Buffer.write('\n')

        except ESCAPE_CONDITION as e:
            #LOG.info(f'ESCAPE: {e}')
            continue


    content = Json_Buffer.getvalue()

    if content is '':
        return (False, "IL2CPP 파일이 동일합니다.")

    f_cmp1.close()
    f_cmp2.close()
    Json_Buffer.close()

    return (content.strip(), (CMP1, CMP2))

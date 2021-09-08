# -*- coding: utf-8 -*-

##################################################################################################

import struct
import disassemble

##################################################################################################


def convSplit(s):
    d = list(s)

    d = ([i+j for i, j in zip(d[::2], d[1::2])])
    for i in range(0,len(d),4):
        d[i:i+4] = list(reversed(d[i:i+4]))

    return ' '.join(d)


def dis(data, arch="ARM"):
    opcode = ''.join([f"\\x{opcode}" for opcode in data.split()]).encode()
    opcode = opcode.decode('unicode-escape').encode('ISO-8859-1')

    return getattr(disassemble, f'disasm{arch}')(opcode)


def getBinay(fr, p, size):
    sig = {2: "<H", 4: "<L", 8: "<Q"}

    fr.seek(p, 0)
    content = fr.read(size)
    return struct.unpack(sig[size], content)[0] if content else None

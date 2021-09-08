# -*- coding:utf-8 -*-

##################################################################################################

import json

import ida_auto

import idaapi
import idautils
import idc

from Logger import LOG

##################################################################################################

d = dict()

##################################################################################################

def getDictStrings():
    for i in idautils.Strings():
        if i.strtype == 0:           # idaapi.STRTYPE_C
            yield {"name": str(i), "offset": i.ea, "lenght": i.length, "type": "ASCII"}
        elif i.strtype == 1:         # idaapi.STRTYPE_C_16
            yield {"name": str(i), "offset": i.ea, "lenght": i.length, "type": "UNICODE"}
        else:
            yield {"name": str(i), "offset": i.ea, "lenght": i.length, "type": "NONE"}


if len(idc.ARGV) != 3:
    LOG.info("[*] [application] [MD5] [SAVE PATH]")
    idc.qexit(0)
    exit(0)
else:
    md5         = idc.ARGV[1]
    SAVE_PATH   = idc.ARGV[2]


LOG.info("Start Get String")
ida_auto.auto_wait()


for i, s in enumerate(getDictStrings()):
    s["md5"] = md5
    d.update({i: s})


with open(SAVE_PATH, 'w') as fw:
    json.dump(dict({"row": d}), fw)


idc.qexit(0)
LOG.info("Main End")

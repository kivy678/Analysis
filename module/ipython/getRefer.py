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


def getAddr():
    for s in idautils.Strings():
        yield s.ea

    for ea in idautils.Functions():
        yield ea


def getReference(addr):
    for xref in idautils.XrefsTo(addr, 1):
        xtype = idautils.XrefTypeName(xref.type)
        if xtype == 'Ordinary_Flow':
            continue
        else:
            yield {"to": xref.to, "from": xref.frm, "type": xtype}


if len(idc.ARGV) != 3:
    LOG.info("[*] [application] [MD5] [SAVE PATH]")
    idc.qexit(0)
    exit(0)
else:
    md5         = idc.ARGV[1]
    SAVE_PATH   = idc.ARGV[2]


LOG.info("Start Get Reference")
ida_auto.auto_wait()


for i, ea in enumerate(getAddr()):
    for s in getReference(ea):
        s["md5"] = md5
        d.update({i: s})


with open(SAVE_PATH, 'w') as fw:
    json.dump(dict({"row": d}), fw)


idc.qexit(0)
LOG.info("Main End")

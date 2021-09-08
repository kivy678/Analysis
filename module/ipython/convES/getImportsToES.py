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

def getImports():
    for i in range(idaapi.get_import_module_qty()):
        dllname = idaapi.get_import_module_name(i)
        if not dllname:
            continue

        entries = []
        def cb(ea, name, ordinal):
            entries.append((ea, name, ordinal))
            return True

        idaapi.enum_import_names(i, cb)
        for ea, name, ordinal in entries:
            yield {"name": dllname, "function": name}


if len(idc.ARGV) != 3:
    LOG.info("[*] [application] [MD5] [SAVE PATH]")
    idc.qexit(0)
    exit(0)
else:
    md5         = idc.ARGV[1]
    SAVE_PATH   = idc.ARGV[2]


LOG.info("Start Get Imports")
ida_auto.auto_wait()


for i, s in enumerate(getImports()):
    s["md5"] = md5
    d.update({i: s})


with open(SAVE_PATH, 'w') as fw:
    json.dump(dict({"row": d}), fw)


idc.qexit(0)
LOG.info("Main End")

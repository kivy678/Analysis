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

def getFuctionList():
    for ea in idautils.Functions():
        fpnt = idaapi.get_func(ea)
        fSize = idaapi.calc_func_size(fpnt)
        name = idaapi.get_func_name(ea)
        #ordinal = idaapi.get_func_num(ea)

        yield (ea, name, fSize)


def getOpcodeFromFunction(ea):
    binary      = dict()
    bin_offset  = dict()
    bin_size    = dict()
    opcode      = dict()

    for j, (startea, endea) in enumerate(idautils.Chunks(ea)):
        bin_list            = list()
        bin_offset_list     = list()
        bin_size_list       = list()
        opcode_list         = list()

        for head in idautils.Heads(startea, endea):
            bin_list.append('{0}'.format(idc.get_bytes(head, idc.get_item_size(head)).encode('hex')))
            bin_offset_list.append(head)
            bin_size_list.append(idc.get_item_size(head))
            opcode_list.append(','.join([idc.print_insn_mnem(head), idc.print_operand(head, 0), idc.print_operand(head, 1)]))


        binary.update({j:       tuple(bin_list)})
        bin_offset.update({j:   tuple(bin_offset_list)})
        bin_size.update({j:     tuple(bin_size_list)})
        opcode.update({j:       tuple(opcode_list)})


        yield (j, bin_list, bin_offset_list, bin_size_list, opcode_list)


if len(idc.ARGV) != 3:
    LOG.info("[*] [application] [MD5] [SAVE PATH]")
    idc.qexit(0)
    exit(0)
else:
    md5         = idc.ARGV[1]
    SAVE_PATH   = idc.ARGV[2]


LOG.info("Start Get Function")
ida_auto.auto_wait()

for i, (ea, name, fSize) in enumerate(getFuctionList()):
    for j, binary, bin_offset, bin_size, opcode in getOpcodeFromFunction(ea):
        d.update({i: {
            "md5":          md5,
            "name":         "{0}.{1}".format(name, j),      # func.1 , func.2 , func.3 ...
            "size":         fSize,
            "binary":       binary,
            "bin_offset":   bin_offset,
            "bin_size":     bin_size,
            "opcode":       opcode
            }
        })


with open(SAVE_PATH, 'w') as fw:
    json.dump(dict({"row": d}), fw)


idc.qexit(0)
LOG.info("Main End")

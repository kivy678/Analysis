# -*- coding: utf-8 -*-

##################################################################################################

try: import simplejson as json
except ImportError: import json

import struct

from util.Logger import LOG
from module.ipython.disasm_view import *

##################################################################################################

script_key = [
    "ScriptMethod",              # "Address", "Name", "Signature"
    #"ScriptMetadataMethod",     # "Address", "Name", "MethodAddress"
    #"ScriptString",             # "Address", "Value"
    #"ScriptMetadata",
    #"Addresses"
]

STRING_FILTER = [
    "Microsoft",
    "MS",
    "Firebase",
    "System",
    "Method$System",
    "Method$UnityEngine",
    "Adverty",
    "anzu",
    "Photon",
    "Quantum",
    "Unity",
    "Mono",
]

rSize = {"THUMB": 2, "ARM": 4, "ARM64": 4}

##################################################################################################


def stringFilter(data, rkey):
    tmpList = list()

    for row in data:
        try:
            for f in STRING_FILTER:
                if row[rkey].startswith(f) is True:
                    raise

            tmpList.append(row)

        except:
            continue

    return tmpList


def parserScriptJson(il2cpp, rpath, wpath, arch="ARM"):

    LOG.info(f"{'[*]':<5}Start Filter Json")

    il2cpp_fr = open(il2cpp, 'rb')

    cnt = 0
    d = dict()

    with open(rpath, encoding='utf-8') as fr:
        j = json.load(fr)
        del(j["ScriptMetadata"])
        del(j["Addresses"])
        del(j["ScriptString"])
        del(j["ScriptMetadataMethod"])

        j['ScriptMethod']           = stringFilter(j['ScriptMethod'], 'Name')
        #j['ScriptMetadataMethod']   = stringFilter(j['ScriptMetadataMethod'], 'Name')

        #############################################################################

        for row in j['ScriptMethod']:
            p = row["Address"]
            rsize = rSize[arch]

            # dis 결과 값이 [offset] [code] [op1][op2] 고정이여서 파싱을 할 수 밖에 없다
            bin_data1 = convSplit(f"{getBinay(il2cpp_fr, p, rsize):0{rsize*2}x}")
            bin_data2 = convSplit(f"{getBinay(il2cpp_fr, p+rsize, rsize):0{rsize*2}x}")
            row["binary"] = f"{bin_data1} {bin_data2}"

            try:
                disasm1, disasm2, _ = tuple(dis(row["binary"], arch=arch).split('\n'))
            except ValueError as e:
                continue        # offset이 0인 경우 디스어셈블리 실패 하기 때문에 예외 발생

            disasm1 = disasm1.split('\t')
            del(disasm1[0])
            del(disasm1[1])

            disasm2 = disasm2.split('\t')
            del(disasm2[0])
            del(disasm2[1])

            row["disasm"] = [','.join(disasm1), ','.join(disasm2)]
            row["Address"] = hex(p)

            d.update({cnt: row})
            cnt +=1

        #############################################################################
        """
        for row in j['ScriptMetadataMethod']:
            del(row["Address"])
            p = row["MethodAddress"]

            bin_data1 = convSplit(f"{getBinay(il2cpp_fr, p, rsize):0{rsize*2}x}")
            bin_data2 = convSplit(f"{getBinay(il2cpp_fr, p+rsize, rsize):0{rsize*2}x}")
            row["binary"] = f"{bin_data1} {bin_data2}"

            try:
                disasm1, disasm2, _ = tuple(dis(row["binary"]).split('\n'))
            except ValueError as e:
                continue

            disasm1 = disasm1.split('\t')
            del(disasm1[0])
            del(disasm1[1])

            disasm2 = disasm2.split('\t')
            del(disasm2[0])
            del(disasm2[1])

            row["disasm"] = [','.join(disasm1), ','.join(disasm2)]
            row["Address"] = hex(row["MethodAddress"])

            d.update({cnt: row})
            cnt +=1

        #############################################################################

        for row in j['ScriptString']:
            row["Address"] = hex(row["Address"])

            d.update({cnt: row})
            cnt +=1
        """
        #############################################################################


    with open(wpath, 'w') as fw:
        json.dump({'row': d}, fw, indent=2, separators=(',', ': '))


    il2cpp_fr.close()

    LOG.info(f"{'[*]':<5}End Filter Json")

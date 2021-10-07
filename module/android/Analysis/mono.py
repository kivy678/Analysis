# -*- coding:utf-8 -*-

#############################################################################

import re
import sys
from io import StringIO

import difflib
import pandas as pd

from util.fsUtils import *
from util.hash import *
from util.Logger import LOG

#############################################################################

EXCEPT_FILE     = ['Assembly-CSharp.csproj', 'Assembly-CSharp.sln']
FILTER_STRING   = ['Assembly-CSharp.dll']

#############################################################################

class ESCAPE_CONDITION(Exception):
    pass

def startCmp(CMP_DIR1, CMP_DIR2):
    comp1 = BaseName(DirName(CMP_DIR1))
    comp2 = BaseName(DirName(CMP_DIR2))

    cmp_dict1 = dict()
    cmp_set1 = set()

    cmp_dict2 = dict()
    cmp_set2 = set()

    for path in Walk(CMP_DIR1):
        cmp_dict1.update( {getSHA256(path): path} )


    for path in Walk(CMP_DIR2):
        cmp_dict2.update( {getSHA256(path): path} )

    cmp_set1 = set(cmp_dict1.keys())
    cmp_set2 = set(cmp_dict2.keys())


    COLUMNS_NAME = [
        'cmp1',
        'cmp2',
        'cmp1_path',
        'cmp2_path',
    ]

    df = pd.DataFrame(columns=COLUMNS_NAME)
    df.index.name = 'fileName'

    for sha256 in cmp_set1.symmetric_difference(cmp_set2):
        filePath = cmp_dict1.get(sha256)
        if (filePath is not None) and                                   \
            (PathSplit(filePath)[1] not in EXCEPT_FILE):
            df.loc[PathSplit(filePath)[1], 'cmp1'] = sha256
            df.loc[PathSplit(filePath)[1], 'cmp1_path'] = filePath

        filePath = cmp_dict2.get(sha256)
        if (filePath is not None) and                                   \
            (PathSplit(filePath)[1] not in EXCEPT_FILE):
            df.loc[PathSplit(filePath)[1], 'cmp2'] = sha256
            df.loc[PathSplit(filePath)[1], 'cmp2_path'] = filePath


    with StringIO() as fw:
        for index in df.index.tolist():
            with open(df.loc[index, 'cmp1_path'], encoding="utf-8") as fr:
                text1 = fr.readlines()

            with open(df.loc[index, 'cmp2_path'], encoding="utf-8") as fr:
                text2 = fr.readlines()

            try:
                tmpString = []
                for s in difflib.unified_diff(text1, text2,                     \
                    fromfile=comp1+': '+index, tofile=comp2+': '+index, n=0, lineterm='\n'):
                    filter_list = list(filter(lambda x: re.search(x, s), FILTER_STRING))

                    if len(filter_list) > 0:
                        raise ESCAPE_CONDITION(''.join(filter_list))
                    else:
                        tmpString.append(s)

            except ESCAPE_CONDITION as e:
                #LOG.info(e)
                continue

            fw.write(''.join(tmpString))
            fw.write('*'*150 + '\n\n')

        return fw.getvalue()

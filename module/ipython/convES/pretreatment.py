# -*- coding:utf-8 -*-

#############################################################################

import json
import subprocess as sub

from common import getSharedPreferences
from webConfig import SHARED_PATH, ES_URL

from util.fsUtils import Join, SplitExt, FileSize

from util.Logger import LOG

#############################################################################

#############################################################################

def pushES(data, index):
    LOG.info(f"{'':>5}Start {index} To ES")
    JSON_PATH = SplitExt(data)[0] + '.json'

    with open(JSON_PATH, 'w') as fw:
        with open(data) as fr:
            j = json.load(fr)
            row = j['row']

            for i in row:
                json.dump({"create": {}}, fw)
                fw.write('\n')

                json.dump(row[i], fw)
                fw.write('\n')

    if FileSize(JSON_PATH) == 0:
        return False

    cmd = f'curl -XDELETE "{ES_URL}/{index}"'
    sub.Popen(cmd).wait()

    cmd = f'curl -XPOST "{ES_URL}/{index}/AndroidOS/_bulk?pretty" -H "Content-Type: application/x-ndjson" --data-binary @{JSON_PATH}'
    sub.Popen(cmd).wait()

    #cmd = f'curl -XGET "{ES_URL}/ida/_search?pretty"'
    #sub.Popen(cmd).wait()

    return True

#############################################################################

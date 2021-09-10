# -*- coding:utf-8 -*-

#############################################################################

import os
import glob

import yara

from util.fsUtils import Join

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.Logger import LOG

#############################################################################

BASE            = os.path.dirname(os.path.realpath(__file__))
RULE_DIR        = Join(BASE, 'rule')

sp              = getSharedPreferences(SHARED_PATH)
MOEMORY_DIR     = Join(sp.getString('ANALYSIS_DIR'), 'MEMORY')

#############################################################################

def run(pkg, rule):
    LOG.info(f"{'[*]':<5}Yara Search Start")
    rules = yara.compile(filepath=Join(RULE_DIR, rule))

    for dump in glob.glob(Join(MOEMORY_DIR, pkg, '*')):
        with open(dump, 'rb') as fr:
            if rules.match(data=fr.read()):
                yield dump

    LOG.info(f"{'[*]':<5}Yara Search End")

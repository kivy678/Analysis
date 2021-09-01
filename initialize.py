# -*- coding:utf-8 -*-

##################################################################################################

__version__ = '0.0.1'

##################################################################################################

import platform

import argparse
import configparser

from common import getSharedPreferences
from util.fsUtils import *

from webConfig import *
from util.Logger import LOG

from util.Logger import LOG

##################################################################################################

for dirName in [LOGGER_PATH, SHARED_PATH_DIR]:
    DirCheck(dirName)

##################################################################################################

sp                  = getSharedPreferences(SHARED_PATH)

config              = configparser.ConfigParser()
config.read(GLOBAL_SETTINGS)

WORKING_DIR         = config['WORK'].get('WORKING_DIR')

##################################################################################################

DATA_DIR            = Join(WORKING_DIR, 'data')
TMP_DIR             = Join(WORKING_DIR, 'tmp')
SAMPLE_DIR          = Join(WORKING_DIR, 'sample')

##################################################################################################

system_os           = platform.system()
arch, _             = platform.architecture()

ed                  = sp.edit()
ed.putString("OS",    system_os)
ed.putString("ARCH",  f'x{arch[:2]}')
ed.commit()

##################################################################################################

JADX_PATH           = config['TOOL'].get('JADX')
IDA_PATH            = config['TOOL'].get('IDA')

##################################################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Android Analysis', description='Android Analysis System')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {0}'.format(__version__))

    parser.add_argument('-i', '--init', action='store_true',
                        help='init', dest='i')

    parser.add_argument('-c', '--clear', action='store_true',
                        help='clear', dest='c')

    args = parser.parse_args()

    if args is None:
        parser.print_help()
        exit()

    if args.i:
        LOG.info(f"{'':>5}[*] INIT SETTING")

        Delete(WORKING_DIR)

        for dirName in [WORKING_DIR, DATA_DIR, TMP_DIR, SAMPLE_DIR]:
            DirCheck(dirName)

        ed = sp.edit()
        ed.putString('WORKING_DIR', WORKING_DIR)
        ed.putString('DATA_DIR', DATA_DIR)

        ed.putString('TMP_DIR', TMP_DIR)
        ed.putString('SAMPLE_DIR', SAMPLE_DIR)

        ed.putString('JADX_PATH', JADX_PATH)
        ed.putString('IDA_PATH', IDA_PATH)

        ed.putBoolean('INIT_SETTING', True)
        ed.commit()

    if args.c:
        pass

    print("Main Done...")

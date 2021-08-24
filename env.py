# -*- coding:utf-8 -*-

import platform
import os
import sys

import runpy
import imp

imp.reload(sys)
# sys.setdefaultencoding('utf-8')

ENV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

if 'Windows' == platform.system():
    ENV_PATH = os.path.join(ENV_DIR, 'Scripts', 'activate_this.py')
else:
    ENV_PATH = os.path.join(ENV_DIR, 'bin', 'activate_this.py')

file_globals = runpy.run_path(ENV_PATH)


import requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

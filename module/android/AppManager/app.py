# -*- coding:utf-8 -*-

###########################################################################################

from datetime import datetime, timedelta

from util.fsUtils import *
from util.parser import *

from database.structure import STATUS
from module.android.cmd import shell

from common import getSharedPreferences
from webConfig import SHARED_PATH

################################################################################

sp                  = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR          = sp.getString('SAMPLE_DIR')
TMP_DIR             = sp.getString('TMP_DIR')

JADX_PATH           = sp.getString('JADX_PATH')

################################################################################

class APP_INFOR:
    def __init__(self):
        self._sha256 = None
        self._pkg    = None
        self._icon   = None
        self._ctime  = None
        self._parent = None
        self._status = None

    def __del__(self):
        Delete(TMP_DIR)
        DirCheck(TMP_DIR)

    def __getattr__(self, key):
        try:
            return self.__dict__[key]
        except KeyError as e:
            return None

    def getResource(self, f):
        app_path = Join(SAMPLE_DIR, f)
        decomp_path = Join(TMP_DIR, f)
        shell.runCommand(f'{JADX_PATH} -s -d {decomp_path} {app_path}')

        return decomp_path

    def parser(self, p):
        if isinstance(p, XmlParser):
            self._pkg     = p.getPackageName()
            self._icon    = p.getIconName()
            self._ctime   = datetime.now().strftime("%Y-%m-%d")
            self._status  = STATUS.INIT.value

        elif isinstance(p, JsonParser):
            pass

    @property
    def sha256(self):
        return self._sha256

    @sha256.setter
    def sha256(self, sha256):
        self._sha256 = sha256

    @property
    def pkg(self):
        return self._pkg

    @property
    def icon(self):
        return self._icon

    @property
    def ctime(self):
        return self._ctime

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

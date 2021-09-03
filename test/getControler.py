from util.Logger import LOG
from util.fsUtils import *
from util.hash import getSHA256

from common import getSharedPreferences
from webConfig import SHARED_PATH

sp                  = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR          = sp.getString('SAMPLE_DIR')

from module.android.AppManager.controler import *
from module.android.AppManager.debug import *




path = Join(SAMPLE_DIR, '4f21454e04037b3fe3b78808c01edeff50c5db680b42c879888cbe2d4de5f2c7')

#appInstall(path)
#appUninstall('com.yeecall')
#p = appDownload('com.yeecall', path)
#print(p)


debugger(path)


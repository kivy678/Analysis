from util.Logger import LOG
from util.fsUtils import *
from util.hash import getSHA256

from common import getSharedPreferences
from webConfig import SHARED_PATH

sp                  = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR          = sp.getString('SAMPLE_DIR')

from module.android.AppManager.controler import *
from module.android.AppManager.debug import *


path = Join(SAMPLE_DIR, 'grow-castle-mod_1.24.2-android-1.com.apk')

#appInstall(path)
#appUninstall('com.yeecall')
#p = appDownload('com.yeecall', path)
#print(p)
#debugger(path)

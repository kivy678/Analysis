from module.android.AppManager.app import APP_INFOR
from util.parser import XmlParser

from util.Logger import LOG
from util.fsUtils import *
from util.hash import getSHA256

from common import getSharedPreferences
from webConfig import SHARED_PATH

sp                  = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR          = sp.getString('SAMPLE_DIR')



path = r'E:\tmp\work\sample\grow-castle-mod_1.24.2-android-1.com.apk'
app_obj = APP_INFOR()
res_path = app_obj.getResource(BaseName(path))

app_obj.parser(XmlParser(res_path))
app_obj.sha256 = getSHA256(path)


print(app_obj.sha256)
print(app_obj.pkg)
print(app_obj.icon)

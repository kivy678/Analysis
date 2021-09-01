from module.android.cmd.adb import *
from module.android.DeviceManager.list.base import DEVICE_MANAGER
from module.android.DeviceManager.list.emulator import LDPlayer


devicesObject = [DEVICE_MANAGER.getPlatform(name=n) for n in getDeviceList()]
print(devicesObject)

ldObject = LDPlayer.list()
print(ldObject)

processer = devicesObject[0].getProcessInfor()
pList = processer.getProcList()


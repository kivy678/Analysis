# -*- encoding: utf-8 -*-

#############################################################################

import pickle

from app.device import blueprint
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

from module.android.cmd.adb import *
from module.android.DeviceManager.list.base import DEVICE_MANAGER
from module.android.DeviceManager.list.emulator import LDPlayer

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.fsUtils import Join

from app.session import setSession
from module.android.cmd import shell

import elfformat

################################################################################

sp                  = getSharedPreferences(SHARED_PATH)
DATA_DIR            = sp.getString('DATA_DIR')

FILE_LIST = ["/system/lib/libc.so"]

################################################################################

@blueprint.route('/device', methods=['GET'])
@login_required
def device():
    try:
        if request.method == 'GET':
            action = request.args.get('btn')
            if action == 'load':
                devicesObject, ldObject, pList, dev_name = load()
                libs = getLib()

                return render_template('device.html', segment='device',
                                                      devices=devicesObject,
                                                      plist_dev=dev_name,
                                                      plist=pList,
                                                      ldplayer=ldObject,
                                                      libs=libs)

        elif request.method == 'POST':
            model_list = request.form.getlist('model')
            if model_list:
                for ld in model_list:
                    LDPlayer.run(ld)

                return "OK"

            if request.form.get('set'):
                devicesName = pickle.loads(getSession('DevName'))
                if devicesName:
                    for name in devicesName:
                        devObj = DEVICE_MANAGER.getPlatform(name=name)
                        devObj.install()

                return "SET"

            return "NOT"

        return render_template('device.html', segment='device')

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        return render_template('page-500.html'), 500

def load():
    # adb device
    devicesObject = [DEVICE_MANAGER.getPlatform(name=n) for n in getDeviceList()]
    ldObject = LDPlayer.list()

    for obj in devicesObject:
        processer = obj.getProcessInfor()
        pList = processer.getProcList()
        dev_name = obj.name
        break

    setSession('DevName', pickle.dumps([dev.name for dev in devicesObject]))

    return (devicesObject, ldObject, pList, dev_name)

def getLib():
    cmd = f"adb pull {FILE_LIST[0]} {DATA_DIR}"
    shell.runCommand(cmd, shell=False)

    libc_path = Join(DATA_DIR, "libc.so")
    data = list()

    for i in elfformat.parser(libc_path, 'dS', 'f').strip().split('\n'):
        try:
            v = i.rstrip('\r').split()
            if v[3] == "FUNC":
                data.append({"func": v[5], "addr": v[1]})

        except IndexError as e:
            continue

    return data

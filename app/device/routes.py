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

from app.session import *

#############################################################################

@blueprint.route('/device', methods=['GET'])
@login_required
def device():
    try:
        action = request.args.get('load')



        return render_template('device.html', segment='device')

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        return render_template('page-500.html'), 500






def load():
    # adb device
    if request.method == 'GET':
        devicesObject = [DEVICE_MANAGER.getPlatform(name=n) for n in getDeviceList()]
        ldObject = LDPlayer.list()

        for obj in devicesObject:
            processer = obj.getProcessInfor()
            pList = processer.getProcList()
            dev_name = obj.name
            break

        setSession('DevName', pickle.dumps([dev.name for dev in devicesObject]))
 
            return render_template('device.html', segment='device',
                                              devices=devicesObject,
                                              plist_dev=dev_name,
                                              plist=pList,
                                              ldplayer=ldObject)


def popst():
    try:
        if request.method == 'POST':
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


    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        return render_template('page-500.html'), 500

# -*- encoding: utf-8 -*-

#############################################################################

import pickle

from app.device import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

from module.android.cmd.adb import *
from module.android.DeviceManager.list.base import DEVICE_MANAGER
from module.android.DeviceManager.list.emulator import LDPlayer

from app.session import *

#############################################################################

@blueprint.route('/<template>', methods=['GET', 'POST'])
@login_required
def device(template):
    try:
        if not template.endswith( '.html' ):
            template += '.html'
        segment = get_segment( request )

        # adb device
        if request.method == 'GET':
            devicesObject = [DEVICE_MANAGER.getPlatform(name=n) for n in getDeviceList()]
            ldObject = LDPlayer.list()

            processer = devicesObject[0].getProcessInfor()
            pList = processer.getProcList()

            setSession('DevName', pickle.dumps([dev.name for dev in devicesObject]))
 
            return render_template( template, segment=segment,
                                              devices=devicesObject,
                                              plist_dev=devicesObject[0].name,
                                              plist=pList,
                                              ldplayer=ldObject)

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


    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        return render_template('page-500.html'), 500


def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'dashboard'

        return segment

    except:
        return None  

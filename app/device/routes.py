# -*- encoding: utf-8 -*-

#############################################################################

from app.device import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

from module.android.cmd.adb import *
from module.android.DeviceManager.list.base import DEVICE_MANAGER
from module.android.DeviceManager.list.emulator import LDPlayer

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
            deviceObject = [DEVICE_MANAGER.getPlatform(name=n) for n in getDeviceList()]
            ldObject = LDPlayer.list()
 
            return render_template( template, segment=segment,
                                              devices=deviceObject,
                                              ldplayer=ldObject)

        elif request.method == 'POST':
            for ld in request.form.getlist('model'):
                LDPlayer.run(ld)
                return "OK"

            if request.form.get('set'):
                # must need global values
                for dev in deviceObject:
                    dev.install()

                return "SET"

            return "END"


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

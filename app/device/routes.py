# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.device import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

from module.android.cmd.adb import *
from module.android.DeviceManager.list.base import DEVICE_BASIS
from module.android.DeviceManager.list.emulator import LDPlayer


@blueprint.route('/<template>')
@login_required
def device(template):
    # adb device
    deviceObject = [DEVICE_BASIS.getPlatform(name=n) for n in getDeviceList()]
    ldObject = LDPlayer.list()


    #

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment,
                                            devices=deviceObject,
                                            ldplayer=ldObject)

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500


def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'dashboard'

        return segment

    except:
        return None  

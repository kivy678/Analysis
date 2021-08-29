# -*- coding:utf-8 -*-

##########################################################################

import pandas as pd

from flask.views import MethodView
from flask import render_template, request

from web.views.device import view

from module.mobile.DeviceManager.device import EMULATOR
from module.database import df_dev

from module.mobile.DeviceManager.analysis import AnalysisData

from util.Logger import LOG

##########################################################################


class DEVICE_WORKER(MethodView):
    def get(self):
        model = request.args['model']
        dev = EMULATOR.getPlatform()

        if dev.setup() is False:
            return "NOT CONNECT DEVICE"

        installer = dev.installer

        if installer.isCommit() is False:

            LOG.info(f"{'[*]':<5}Settings Start")
            installer.serverDecompress()
            installer.toolDecompress()
            installer.userToolDecompress()

            LOG.info(f"{'':>5}1. Basis App Install Start")
            installer.appInstaller()

            LOG.info(f"{'':>5}2. Cow Exploit Start")
            installer.cowExploit()

            LOG.info(f"{'':>5}3. Frida Server Install Start")
            installer.fridaServer()

            LOG.info(f"{'':>5}4. Android Server Install Start")
            installer.androidServer()

            LOG.info(f"{'':>5}5. Tool Install Start")
            installer.toolInstall()

            LOG.info(f"{'':>5}6. User Tool Install Start")
            installer.userToolInstall()

            LOG.info(f"{'':>5}6. Device Data Get Analysis to Start")
            analysiser = AnalysisData(dev)
            analysiser.getData()

            LOG.info(f"{'':>5}7. Commit To Device")
            installer.commit()

            LOG.info(f"{'[*]':<5}Settings End")
            df_dev.DATA_FRAME.loc[df_dev.DATA_FRAME['model'] == model, 'setup'] = True

            return "Settings End"
        else:
            LOG.info(f"{'[*]':<5}Has Initalize Device")

            return "Has Initalize Device"


device = DEVICE_WORKER.as_view('work')
view.add_url_rule('work', view_func=device)

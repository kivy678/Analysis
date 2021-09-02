# -*- encoding: utf-8 -*-

#############################################################################

import glob

from app.app import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

from flask import send_from_directory
from werkzeug.utils import secure_filename

from module.android.AppManager.decompiler import *
from module.android.AppManager.app import APP_INFOR
from util.parser import XmlParser

from util.Logger import LOG
from util.fsUtils import *
from util.hash import getSHA256

from database.models import *
from app import db

from common import getSharedPreferences
from webConfig import SHARED_PATH

################################################################################

sp                  = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR          = sp.getString('SAMPLE_DIR')

################################################################################


@blueprint.route('/app', methods=['GET', 'POST'])
@login_required
def app():
    try:
        sample_list = [BaseName(path) for path in glob.glob(Join(SAMPLE_DIR, '*'))]

        if request.method == 'GET':
            return render_template('app.html', segment='app',
                                             sample_infor=APP.query.all())
        elif request.method == 'POST':
            f = request.files['file']
            f_path = Join(SAMPLE_DIR, secure_filename(f.filename))
            f.save(f_path)

            updateSample(f_path)
            #Delete(f_path)

            return "OK"

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        return render_template('page-500.html'), 500


@blueprint.route('/app/infor/<sha256>', methods=['GET', 'POST'])
@login_required
def infor(sha256):
    try:
        if request.method == 'POST':
            decode_tool = request.form.get('decode')
            tool = {'unzip': runUnzip, 'apktool': runApktool, 'androg': runAndrog, 'jadx': runJadx}
            tool[decode_tool](Join(SAMPLE_DIR, sha256))

        return render_template('infor.html', segment='infor', app_infor=APP.query.filter_by(sha256=sha256))


    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        return render_template('page-500.html'), 500


def updateSample(f_path):
    app_obj = APP_INFOR()
    res_path = app_obj.getResource(BaseName(f_path))

    app_obj.parser(XmlParser(res_path))
    app_obj.sha256 = getSHA256(f_path)

    form = {
        'sha256': app_obj.sha256,
        'pkg': app_obj.pkg,
        'icon': app_obj.icon,
        'ctime': app_obj.ctime,
        'parent': 1,
        'status': app_obj.status
    }

    try:
        app = APP(**form)
        db.session.add(app)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

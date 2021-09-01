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
        segment = get_segment(request)
        template = segment + '.html'

        sample_list = [BaseName(path) for path in glob.glob(Join(SAMPLE_DIR, '*'))]
        #getSample()

        if request.method == 'GET':
            return render_template(template, segment=segment,
                                             sample_infor=APP.query.all())
        elif request.method == 'POST':
            f = request.files['file']
            f_path = Join(SAMPLE_DIR, secure_filename(f.filename))
            f.save(f_path)

            updateSample(f_path)

            return "OK"

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        return render_template('page-500.html'), 500


def get_segment(request):
    try:
        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'device'

        return segment

    except:
        return None  


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

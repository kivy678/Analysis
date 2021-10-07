# -*- encoding: utf-8 -*-

#############################################################################

import glob

from app.compare import blueprint
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

from flask import send_from_directory
from werkzeug.utils import secure_filename

from common import getSharedPreferences
from webConfig import SHARED_PATH

from database.models import *
from util.fsUtils import *

from module.android.Analysis.tree import startCmp
from module.android.Analysis.mono import startCmp
from module.android.Analysis.il2cpp import startCmp
from module.android.Analysis.il2cpp_view import view

################################################################################

sp                  = getSharedPreferences(SHARED_PATH)
SAMPLE_DIR          = sp.getString('SAMPLE_DIR')
DECODE_DIR          = sp.getString('DECODE_DIR')

################################################################################


@blueprint.route('/compare', methods=['GET', 'POST'])
@login_required
def compare():
    try:
        sample_list = [BaseName(path) for path in glob.glob(Join(SAMPLE_DIR, '*'))]

        if request.method == 'GET':
            return render_template('compare.html', segment='compare',
                                             sample_infor=APP.query.all())

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        return render_template('page-500.html'), 500


@blueprint.route('/compare/tree', methods=['GET', 'POST'])
@login_required
def tree():
    if request.method == 'POST':
        sha256_list = request.form.getlist('sha256')
        file_filter = request.form.getlist('file_filter')

        f = [Join(DECODE_DIR, sha256, 'unzip') for sha256 in sha256_list]

        return startCmp(f[0], f[1], file_filter)


@blueprint.route('/compare/mono', methods=['GET', 'POST'])
@login_required
def mono():
    if request.method == 'POST':
        sha256_list = request.form.getlist('sha256')

        f = [Join(DECODE_DIR, sha256, 'mono') for sha256 in sha256_list]

        return startCmp(f[0], f[1])


@blueprint.route('/compare/il2cpp', methods=['GET', 'POST'])
@login_required
def il2cpp():
    if request.method == 'POST':
        sha256_list = request.form.getlist('sha256')

        f = [Join(DECODE_DIR, sha256, 'unzip') for sha256 in sha256_list]
        f2 = [Join(DECODE_DIR, sha256, 'il2cpp') for sha256 in sha256_list]

        cmp_data, path = startCmp(f[0], f[1])
        if cmp_data is False:
            return path

        view_data, save_data = view(cmp_data, f2[0])

        return view_data


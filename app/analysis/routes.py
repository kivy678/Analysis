# -*- encoding: utf-8 -*-

#############################################################################

import subprocess as sub

from hurry.filesize import size as convSize
from hurry.filesize import alternative

from app.analysis import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

from flask import send_from_directory
from werkzeug.utils import secure_filename

from common import getSharedPreferences
from webConfig import *

import elfformat
from app.session import getSession

from util.fsUtils import *
from util.hash import getMD5

from module.ipython.convES.pretreatment import pushES
from module.ipython.convES.scriptjs import parserScriptJson

from app.analysis.getLib import *
from module.android.Analysis.server import *

################################################################################

sp                  = getSharedPreferences(SHARED_PATH)
DECODE_DIR          = sp.getString('DECODE_DIR')
DATA_DIR            = sp.getString("DATA_DIR")

RUN_PATH            = Join(BASE_DIR, "module", "ipython", "run.bat")
RUN_IL2CPP_PATH     = Join(BASE_DIR, "module", "ipython", "run_il2cpp.bat")

################################################################################


@blueprint.route('/analysis', methods=['GET', 'POST'])
@login_required
def analysis():
    try:
        if request.method == 'GET':
            sha256 = getSession('sha256')

            return render_template('analysis.html', segment='analysis',
                                                    lib_list=lib_List(sha256),
                                                    ida_list=ida_List(sha256))

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        return render_template('page-500.html'), 500


@blueprint.route('/analysis/disasm', methods=['GET'])
@login_required
def disasm():
    if request.method == 'GET':
        arch = request.args.get('arch')
        text = request.args.get('text')

        return fetch_disasm(arch, text)

@blueprint.route('/analysis/format', methods=['GET'])
@login_required
def format():
    if request.method == 'GET':
        lib_path = request.args.get('lib_path')
        lib_type = request.args.get('lib_type')

        sha256 = getSession('sha256')
        lib_path = Join(DECODE_DIR, sha256, 'unzip', lib_path)

        try:
            if lib_type in ['f', 'h', 's', 'd', 'S', 'dS', 'r', 'rp']:
                return elfformat.parser(lib_path, lib_type, 'f')
            else:
                return '\n'.join([i for i in elfformat.parser(lib_path, '', 'f')])

        except Exception as e:
            print(e)
            return "The file is Bad Format."

@blueprint.route('/analysis/ida', methods=['GET'])
@login_required
def ida():
    if request.method == 'GET':
        lib_path = request.args.get('lib_path')

        sha256 = getSession('sha256')
        lib_path = Join(DECODE_DIR, sha256, 'unzip', lib_path)
        md5 = getMD5(lib_path)

        script = "getStringToES.py"
        DATA_PATH = Join(DATA_DIR, md5 + '_str.txt')
        sub.Popen(f"{RUN_PATH} {script} {md5} {DATA_PATH} {lib_path}").wait()
        pushES(DATA_PATH, 'aosstrings')

        script = "getImportsToES.py"
        DATA_PATH = Join(DATA_DIR, md5 + '_imp.txt')
        sub.Popen(f"{RUN_PATH} {script} {md5} {DATA_PATH} {lib_path}").wait()
        pushES(DATA_PATH, 'aosimports')

        script = "getFunctionsToES.py"
        DATA_PATH = Join(DATA_DIR, md5 + '_func.txt')
        sub.Popen(f"{RUN_PATH} {script} {md5} {DATA_PATH} {lib_path}").wait()
        pushES(DATA_PATH, 'aosfunctions')

        return "Success"

@blueprint.route('/analysis/ida/il2cpp', methods=['GET'])
@login_required
def ida_il2cpp():
    if request.method == 'GET':
        sha256 = getSession('sha256')

        il2cpp_path = Join(DECODE_DIR, sha256, 'il2cpp')
        jsonPath    = Join(il2cpp_path, 'script.json')

        unzip_path  = Join(DECODE_DIR, sha256, 'unzip')
        lib_path    = findFile(unzip_path, 'libil2cpp.so')

        md5         = getMD5(lib_path)

        script = "getStringToES.py"
        DATA_PATH = Join(DATA_DIR, md5 + '_str.txt')
        sub.Popen(f"{RUN_IL2CPP_PATH} {jsonPath} {script} {md5} {DATA_PATH} {lib_path}").wait()
        pushES(DATA_PATH, 'aosstrings')

        script = "getImportsToES.py"
        DATA_PATH = Join(DATA_DIR, md5 + '_imp.txt')
        sub.Popen(f"{RUN_IL2CPP_PATH} {jsonPath} {script} {md5} {DATA_PATH} {lib_path}").wait()
        pushES(DATA_PATH, 'aosimports')

        script = Join(BASE_DIR, "module", "ipython", "getFunctionsToES.py")
        DATA_PATH = Join(DATA_DIR, md5 + '_func.txt')
        sub.Popen(f"{RUN_IL2CPP_PATH} {jsonPath} {script} {md5} {DATA_PATH} {lib_path}").wait()
        pushES(DATA_PATH, 'aosfunctions')

        return "Success"


@blueprint.route('/analysis/il2cpp', methods=['GET'])
@login_required
def il2cpp():
    if request.method == 'GET':
        sha256 = getSession('sha256')
        arch        = request.args.get("arch")

        il2cpp_path = Join(DECODE_DIR, sha256, 'il2cpp')
        jsonPath    = Join(il2cpp_path, 'script.json')

        unzip_path  = Join(DECODE_DIR, sha256, 'unzip')
        lib_path    = findFile(unzip_path, 'libil2cpp.so')

        es_json     = Join(DATA_DIR, getMD5(lib_path) + '_il2cpp.txt')

        parserScriptJson(lib_path, jsonPath, es_json, arch)
        pushES(es_json, 'aosfunctions')

        return "Success"

@blueprint.route('/analysis/settings', methods=['GET'])
@login_required
def settings():
    if request.method == 'GET':
        dynamicServer()

        return "Success"


@blueprint.route('/analysis/strace', methods=['GET'])
@login_required
def strace():
    if request.method == 'GET':
        dynamicServer()

        return "Success"

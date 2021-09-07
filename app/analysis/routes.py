# -*- encoding: utf-8 -*-

#############################################################################

from app.analysis import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

from flask import send_from_directory
from werkzeug.utils import secure_filename

from common import getSharedPreferences
from webConfig import SHARED_PATH

import disassemble
import elfformat
from app.session import getSession

from util.fsUtils import *

################################################################################

sp                  = getSharedPreferences(SHARED_PATH)
DECODE_DIR          = sp.getString('DECODE_DIR')

################################################################################


@blueprint.route('/analysis', methods=['GET', 'POST'])
@login_required
def analysis():
    try:
        if request.method == 'GET':
            return render_template('analysis.html', segment='analysis',
                                                    lib_list=lib_List())

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
            return "잘못된 형식의 파일입니다."

def lib_List():
    data = list()
    sha256 = getSession('sha256')

    if sha256 is None:
        return []

    analysis_path = Join(DECODE_DIR, sha256, 'unzip')

    for path in Walk(analysis_path):
        p = BaseName(path)

        if SplitExt(p)[1] == ".so":
            data.append(path)

    data = map(lambda x: x.replace(analysis_path, '')[1:], data)
    return data

def fetch_disasm(arch, text):
    opcode = ''.join([f"\\x{opcode}" for opcode in text.split()]).encode()
    opcode = opcode.decode('unicode-escape').encode('ISO-8859-1')

    return getattr(disassemble, f'disasm{arch}')(opcode)

# -*- encoding: utf-8 -*-

#############################################################################

from app.analysis import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

from flask import send_from_directory
from werkzeug.utils import secure_filename

import disassemble

################################################################################


@blueprint.route('/analysis', methods=['GET', 'POST'])
@login_required
def analysis():
    try:
        if request.method == 'GET':
            return render_template('analysis.html', segment='analysis')

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except Exception as e:
        return render_template('page-500.html'), 500


@blueprint.route('/analysis/disasm', methods=['GET', 'POST'])
@login_required
def disasm():
    if request.method == 'GET':
        arch = request.args.get('arch')
        text = request.args.get('text')

        return fetch_disasm(arch, text)

def fetch_disasm(arch, text):
    opcode = ''.join([f"\\x{opcode}" for opcode in text.split()]).encode()
    opcode = opcode.decode('unicode-escape').encode('ISO-8859-1')

    return getattr(disassemble, f'disasm{arch}')(opcode)

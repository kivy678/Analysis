# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound

from database.models import DEVICE
from app import db

@blueprint.route('/dashboard')
@login_required
def index():

    return render_template('dashboard.html', segment='dashboard')

@blueprint.route('/<template>')
@login_required
def device(template):
    """
    form = {
        'model': 'android2',
        'cpu': 'x86',
        'sdk': 'android-86',
        'su': True,
        'setup': True
    }

    user = DEVICE(**form)
    db.session.add(user)
    db.session.commit()
    """

    user = DEVICE.query.all()
    for i in user:
        print(i.cpu)

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404

    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'dashboard'

        return segment

    except:
        return None  

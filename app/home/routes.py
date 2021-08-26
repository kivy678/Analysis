# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager

@blueprint.route('/dashboard')
@login_required
def index():
    return render_template('dashboard.html', segment='dashboard')

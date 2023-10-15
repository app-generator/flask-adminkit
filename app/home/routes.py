# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import requests


@blueprint.route('/index')
@login_required
def index():
    response = requests.get('http://127.0.0.1:8000/api/get_informations')  # Remplacez avec l'URL de votre API
    bot_info = response.json()  # Supposons que votre API renvoie un JSON
    bot_username = bot_info[0][1]
    bot_server = bot_info[0][3]
    return render_template('index.html', segment='index', bot_username=bot_username, bot_server=bot_server)

@blueprint.route('/<template>')
@login_required
def route_template(template):

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
            segment = 'index'

        return segment    

    except:
        return None  

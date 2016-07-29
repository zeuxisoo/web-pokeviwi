# coding: utf-8

import json
from os import path
from flask import Flask
from flask import url_for
from .utils import api

def create_app(config=None, enable_route=True):
    app = Flask(__name__, template_folder='views')
    app.static_folder = path.abspath('static')

    www_root = path.dirname(path.dirname(__file__))

    app.config.from_pyfile(
        path.join(www_root, 'config/default.py')
    )

    production_config = path.join(www_root, 'config/production.py')
    if path.exists(production_config):
        app.config.from_pyfile(production_config)

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(path.abspath(config))

    register_pgoapi(app)
    register_jinja2(app)
    register_route(app)

    return app

def register_pgoapi(app):
    app.api = api

def register_jinja2(app):
    @app.context_processor
    def utility_processor():
        def asset_url(filename):
            rev_manifest_path = path.join(app.static_folder, 'build/rev-manifest.json')

            with open(rev_manifest_path, 'r') as f:
                rev_manifest = json.loads(f.read())
                return url_for('static', filename='build/' + rev_manifest[filename])

        return dict(asset_url=asset_url)


def register_route(app):
    from .routes import index
    from .routes import api

    app.register_blueprint(api.player.blueprint, url_prefix='/api/player')
    app.register_blueprint(api.auth.blueprint, url_prefix='/api/auth')
    app.register_blueprint(api.pokemon.blueprint, url_prefix='/api/pokemon')
    app.register_blueprint(index.blueprint, url_prefix='')

# coding: utf-8

from os import path
from flask import Flask

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


    register_jinja2(app)
    register_route(app)

    return app

def register_jinja2(app):
    pass

def register_route(app):
    from .routes import index

    app.register_blueprint(index.blueprint, url_prefix='')

from flask import Flask
from db import db
import importlib
import os
import pandas as pd
from app.models.menu_model import MenuModel


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    for apis in ['app.routers']:
        api = importlib.import_module(apis)
        api.module_api.init_app(app)
    db.init_app(app)

    @app.before_first_request
    def create_table():
        db.create_all()
    return app

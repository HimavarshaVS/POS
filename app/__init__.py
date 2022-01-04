from flask import Flask
from db import db
import importlib
import os
from config import ConfigClass
from app.models.menu_model import MenuModel

def create_app():
    app = Flask(__name__)

    # app.config['SQLALCHEMY_DATABASE_URI'] = ConfigClass.DATABASE_URL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    for apis in ['app.routers']:
        api = importlib.import_module(apis)
        api.module_api.init_app(app)
    db.init_app(app)

    @app.before_first_request
    def create_table():
        db.create_all()
        # test_rec = MenuModel({
        #     "item_name": "4 Mc chicken nuggets",
        #     "description": "nuggets",
        #     "price": 10.96,
        #     "quantity": 100,
        #     "modifiers": {
        #         "toppings": ["Lettuce", "Tomato", "Pickles", "Onions"],
        #         "bun_choice": ["sesame", "whole wheat", "keto"]
        #     }
        # })
        # db.session.add_all(test_rec)
        # db.session.rollback()
        # db.session.commit()

    return app

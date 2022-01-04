from flask import Flask
from db import db
import importlib
import os
from config import ConfigClass
from models.menu_model import MenuModel

def create_app():
    app = Flask(__name__)
    # app.config.from_object(__name__ + '.ConfigClass')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    #     user="varsha",
    #     pw="admin",
    #     url="db:5432",
    #     db="pos")
    # os.getenv("DATABASE_URL"
    print(os.getenv("DATABASE_URL"))
    app.config['SQLALCHEMY_DATABASE_URI'] = ConfigClass.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    for apis in ['routers']:
        api = importlib.import_module(apis)
        api.module_api.init_app(app)
    db.init_app(app)

    @app.before_first_request
    def create_table():
        db.create_all()
        # test_rec = MenuModel([{
        #     "item_name": "4 Mc chicken nuggets",
        #     "description": "nuggets",
        #     "price": 10.96,
        #     "quantity": 100,
        #     "modifiers": {
        #         "toppings": ["Lettuce", "Tomato", "Pickles", "Onions"],
        #         "bun_choice": ["sesame", "whole wheat", "keto"]
        #     }
        # }, {
        #     "item_name": "Filet-O-Fish",
        #     "description": "wrap",
        #     "price": 7.99,
        #     "quantity": 10,
        #     "modifiers": {
        #         "toppings": ["Lettuce", "Tomato", "Pickles", "Onions"],
        #         "wrap": ["sesame", "whole wheat", "keto"]
        #     }
        # }])
        # db.session.add_all(test_rec)
        # db.session.rollback()
        # db.session.commit()

    return app

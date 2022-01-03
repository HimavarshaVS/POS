from flask import Flask
from db import  db
import importlib

def create_app():
    app = Flask(__name__)
    # app.config.from_object(__name__ + '.ConfigClass')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user="varsha",
        pw="admin",
        url="localhost:5432",
        db="data")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    for apis in ['routers']:
        api = importlib.import_module(apis)
        api.module_api.init_app(app)

    @app.before_first_request
    def create_table():
        db.create_all()

    db.init_app(app)
    return app

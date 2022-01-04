from flask_restx import Api
from app.routers.orders.orders_api import *
from app.routers.menu.items_api import *

module_api = Api(
    version='1.0'
)


api = module_api.namespace('pos')

api.add_resource(Menu, '/v1/menu')
api.add_resource(UpdateMenu, '/v1/menu/<item_id>')
api.add_resource(Orders, '/v1/orders')
api.add_resource(FetchOrders, "/v1/orders/<order_id>")

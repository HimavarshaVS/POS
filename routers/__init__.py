from flask_restx import Api
from routers.orders_api import *
from routers.items_api import *

module_api = Api(
    version='1.0'
)


api = module_api.namespace('pos')

api.add_resource(Menu, '/v1/items')
api.add_resource(UpdateMenu, '/v1/items/<item_id>')
api.add_resource(Orders, '/v1/orders')
api.add_resource(FetchOrders, "/v1/orders/<order_id>")

from flask_restx import Api
from routers.orders_api import Orders
from routers.items_api import Menu, UpdateMenu

# from flask_restful import Api
module_api = Api(
    version='1.0'
)


api = module_api.namespace('POS',path ='/')

api.add_resource(Menu, '/v1/items')
api.add_resource(UpdateMenu, '/v1/item/<item_id>')
api.add_resource(Orders, '/v1/orders')

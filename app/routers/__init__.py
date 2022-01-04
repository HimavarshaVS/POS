from flask_restx import Api, fields

module_api = Api(
    version='1.0',
    title='POS System',
    description='APIs designed for a point of sale (POS) system. The POS system has the capability to control the menu and perform CRUD operations also which can place an order successfully by validating the payment correctness and item availability',
    doc='/v1/api-doc'
)


from .endpoints.orders_api import *
menu_api = module_api.namespace('Menu', description='POS menu CRUD operations', path='/')
order_api = module_api.namespace('Orders', description='POS order creation', path='/')

from .endpoints.items_api import *
menu_api.add_resource(Menu, '/v1/item')
menu_api.add_resource(FetchMenu, '/v1/items')
menu_api.add_resource(UpdateMenu, '/v1/item/<item_id>')
order_api.add_resource(Orders, '/v1/order')
order_api.add_resource(FetchOrders, "/v1/order/<order_id>")

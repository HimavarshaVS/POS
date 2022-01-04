from flask_restx import fields

from . import module_api

menu_module = module_api.model('Menu', {
    "item_name": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "quantity": fields.Integer,
    "modifiers": fields.Nested
})

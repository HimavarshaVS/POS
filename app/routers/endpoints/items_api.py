from flask_restx import Resource, fields
from flask import request
from flask_pydantic import validate
from app.commons.service_logger.logger_factory_service import SrvLoggerFactory
from app.commons.utils import *
from app.models.api_response import APIResponse, EAPIResponseCode
from app.models.menu_model import MenuModel
from app.models.base_models import *
from db import db
from ...routers import module_api

_API_NAMESPACE = "Menu"
_logger = SrvLoggerFactory(_API_NAMESPACE).get_logger()


nested_modifier_model = {'Toppings': fields.List(fields.String()), 'Bread': fields.List(fields.String())}

menu_module = module_api.model('MenuModel', {
    "item_name": fields.String(),
    "description": fields.String(),
    "price": fields.Float(),
    "quantity": fields.Integer(),
    "modifiers": fields.Nested(module_api.model('nested_modifier_model', nested_modifier_model))
})


class Menu(Resource):

    @validate()
    @module_api.expect(menu_module, validate=True)
    def post(self, body: ItemBaseModel):
        """ POST method to create new item to the menu"""

        res = APIResponse()
        _logger.info(f"Add a new item to the menu")
        post_data = dict(body)
        required_params = ["description", "price", "quantity"]
        try:
            if not all(key in post_data for key in required_params):
                _logger.error(f"missing required params : {required_params}")
                return return_res(f"missing required params : {required_params}", EAPIResponseCode.bad_request)

            item_info = MenuModel(**post_data)
            db.session.add(item_info)
            db.session.commit()
            db.session.refresh(item_info)
            del item_info.__dict__['_sa_instance_state']
            return return_res({"msg": "Item created successfully", "item_info": item_info.__dict__}, EAPIResponseCode.success)

        except Exception as error:
            error_msg = f"Error while trying to save item to the menu"
            if 'UniqueViolation' in error.args[0]:
                error_msg = f"Item with name {post_data['item_name']} already exists"
                return return_res(f"{error_msg}", EAPIResponseCode.conflict)
            _logger.error(f"{error_msg}: {error}")
            return return_res(f"{error_msg}: {error}", EAPIResponseCode.internal_error)


class FetchMenu(Resource):
    def get(self):
        """ Fetch list of all items in the menu"""
        res = APIResponse()
        _logger.info(f"Fetch all Items from menu")
        try:
            items = []
            for item in db.session.query(MenuModel).all():
                del item.__dict__['_sa_instance_state']
                items.append(item.__dict__)
            if len(items) == 0:
                _logger.error(f"No records found")
                return return_res(f"No records found", EAPIResponseCode.no_records)
            _logger.info(f"Items retrieved successfully")
            return return_res(items, EAPIResponseCode.success)
        except Exception as error:
            _logger.error(f"Error while trying to fetch menu from menu : {error}")
            return return_res(f"Error while trying to fetch menu from menu", EAPIResponseCode.internal_error)


class UpdateMenu(Resource):
    @validate()
    @module_api.expect(menu_module)
    def put(self, item_id: int, body: UpdateItemBaseModel):
        """ Update an item based on item id"""
        res = APIResponse()
        post_data = dict(request.get_json())
        if post_data.get('id', None) is not None:
            return return_res(f"Item id cannot be modified", EAPIResponseCode.bad_request)
        if item_id is None:
            _logger.error(f"Please provide valid item_id to update the item")
            return return_res(f"Please provide valid item_id to update the item", EAPIResponseCode.bad_request)

        try:
            rows_updated = db.session.query(MenuModel).filter_by(id=item_id).update(dict(post_data))
            if rows_updated == 0:
                return return_res(f"Item id {item_id} doesn't exists", EAPIResponseCode.not_found)
            db.session.commit()
            _logger.info(f"Item details updated successfully for item : {item_id}")
            return return_res(f"Item details updated successfully for item : {item_id}", EAPIResponseCode.success)
        except Exception as error:
            _logger.error(f"Error while trying to update item : {error}")
            return return_res(f"Error while trying to update item : {error}", EAPIResponseCode.internal_error)

    @validate()
    def delete(self, item_id: int):
        """ Delete an item based on item id"""
        _logger.info(f"Deleting item : {item_id}")
        res = APIResponse()
        if item_id is None:
            _logger.error(f"Please provide valid item_id to update the item")
        try:
            rows_deleted = db.session.query(MenuModel).filter_by(id=item_id).delete()
            if rows_deleted == 0:
                return return_res(f"Item id {item_id} doesn't exists", EAPIResponseCode.not_found)
            db.session.commit()
            _logger.info(f"Item deleted successfully for item id : {item_id}")
            return return_res(f"Item deleted successfully for item id : {item_id}", EAPIResponseCode.success)
        except Exception as error:
            _logger.error(f"Error while trying to delete data : {error}")
            return return_res(f"Error while trying to delete data ", EAPIResponseCode.internal_error)


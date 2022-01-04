from flask_restx import Resource
from flask import request
from flask_pydantic import validate
from commons.service_logger.logger_factory_service import SrvLoggerFactory
from commons.utils import *
from models.api_response import APIResponse, EAPIResponseCode
from models.menu_model import MenuModel
from models.base_models import *
from db import db


_API_NAMESPACE = "Menu"
_logger = SrvLoggerFactory(_API_NAMESPACE).get_logger()


class Menu(Resource):

    """ POST method to create new item to the menu"""
    @validate()
    def post(self, body: ItemBaseModel):
        res = APIResponse()
        _logger.info(f"Add a new item to the menu")
        post_data = dict(body)
        required_params = ["description", "price", "quantity"]
        try:
            if not all(key in post_data for key in required_params):
                _logger.error(f"missing required params : {required_params}")
                return return_error_res(res,f"missing required params : {required_params}", EAPIResponseCode.bad_request)
            item_info = MenuModel(**post_data)
            db.session.add(item_info)
            db.session.commit()
            db.session.refresh(item_info)
            del item_info.__dict__['_sa_instance_state']
            return return_res({"msg": "Item created successfully", "item_info": item_info.__dict__}, EAPIResponseCode.success)

        except Exception as error:
            error_msg = f"Error while trying to save items to the menu"
            _logger.error(f"{error_msg}: {error}")
            return return_res(f"{error_msg}: {error}", EAPIResponseCode.internal_error)

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
                return return_error_res(res,f"No records found", EAPIResponseCode.no_records)
            _logger.info(f"Items retrieved successfully")
            return return_res(items, EAPIResponseCode.success)
        except Exception as error:
            _logger.error(f"Error while trying to fetch items from menu : {error}")
            return return_error_res(res,f"Error while trying to fetch items from menu", EAPIResponseCode.internal_error)


class UpdateMenu(Resource):
    @validate()
    def put(self, item_id: int, body: UpdateItemBaseModel):
        res = APIResponse()
        post_data = dict(request.get_json())
        if item_id is None:
            _logger.error(f"Please provide valid item_id to update the item")
        try:
            db.session.query(MenuModel).filter_by(id=item_id).update(dict(post_data))
            db.session.commit()
            _logger.info(f"Item details updated successfully for item : {item_id}")
            return return_res(f"Item details updated successfully for item : {item_id}", EAPIResponseCode.success)
        except Exception as error:
            _logger.error(f"Error while trying to update item : {error}")
            return return_res(f"Error while trying to update item", EAPIResponseCode.internal_error)

    @validate()
    def delete(self, item_id: int):
        _logger.info(f"Deleting item : {item_id}")
        res = APIResponse()
        if item_id is None:
            _logger.error(f"Please provide valid item_id to update the item")
        try:
            db.session.query(MenuModel).filter_by(id=item_id).delete()
            db.session.commit()
            _logger.info(f"Item deleted successfully for item id : {item_id}")
            return return_res(f"Item deleted successfully for item id : {item_id}", EAPIResponseCode.success)
        except Exception as error:
            _logger.error(f"Error while trying to delete data : {error}")
            return return_res(f"Error while trying to delete data ", EAPIResponseCode.internal_error)


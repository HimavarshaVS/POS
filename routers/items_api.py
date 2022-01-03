from flask_restx import Resource
from flask_pydantic import validate
from commons.service_logger.logger_factory_service import SrvLoggerFactory
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
        # is_valid, msg = self.validate_payload(post_data)
        required_params = ["description", "price", "quantity"]
        try:
            if not all(key in post_data for key in required_params):
                _logger.error(f"missing required params : {required_params}")
                res.set_result(f"missing required params : {required_params}")
                res.set_code(EAPIResponseCode.bad_request)
                return res.response
            item_info = MenuModel(**post_data)
            db.session.add(item_info)
            db.session.commit()
            res.set_result(F'Item created successfully')
            res.set_code(EAPIResponseCode.success)
            return res.response

        except Exception as error:
            _logger.error(f"Error while trying to save items to the menu {error}")
            res.set_result(f"Error while trying to save items to the menu {error}")
            res.set_code(EAPIResponseCode.internal_error)
            return res.response

    def validate_payload(self, post_data):
        """validate payload params"""
        pass

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
                res.set_result(f"No records found")
                res.set_code(EAPIResponseCode.no_records)
            res.set_result(items)
            res.set_code(EAPIResponseCode.success)
            return res.response
        except Exception as error:
            _logger.error(f"Error while trying to fetch items from menu : {error}")
            res.set_result(f"Error while trying to fetch items from menu")
            res.set_code(EAPIResponseCode.internal_error)
            return res.response


class UpdateMenu(Resource):
    @validate()
    def put(self, item_id: int, body: UpdateItemBaseModel):
        res = APIResponse()
        post_data = dict(body)
        if item_id is None:
            _logger.error(f"Please provide valid item_id to update the item")
        try:
            db.session.query(MenuModel).filter_by(id=item_id).update(dict(post_data))
            db.session.commit()
            res.set_result(f"Item details updated successfully for item : {item_id}")
            res.set_code(EAPIResponseCode.success)
            return res.response
        except Exception as error:
            _logger.error(f"Error while trying to update item : {error}")
            res.set_result(f"Error while trying to update item")
            res.set_code(EAPIResponseCode.internal_error)
            return res.response

    @validate()
    def delete(self, item_id: int):
        res = APIResponse()
        if item_id is None:
            _logger.error(f"Please provide valid item_id to update the item")
        try:
            db.session.query(MenuModel).filter_by(id=item_id).delete()
            db.session.commit()
            res.set_result(f"Item deleted successfully for item id : {item_id}")
            res.set_code(EAPIResponseCode.success)
            return res.response
        except Exception as error:
            _logger.error(f"Error while trying to delete data : {error}")
            res.set_result(f"Error while trying to delete data")
            res.set_code(EAPIResponseCode.internal_error)
            return res.response

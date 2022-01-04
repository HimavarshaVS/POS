from flask_restx import Resource, fields
from flask_pydantic import validate
from app.commons.service_logger.logger_factory_service import SrvLoggerFactory
from app.commons.utils import *
from app.models.api_response import APIResponse, EAPIResponseCode
from app.models.menu_model import OrderModel, MenuModel
from app.models.base_models import *
from db import db
import pandas as pd
from ...routers import module_api

_API_NAMESPACE = "Orders"
_logger = SrvLoggerFactory(_API_NAMESPACE).get_logger()

nested_item_model = {}
nested_item_model['item_id'] = fields.Integer()
nested_item_model['quantity'] = fields.Integer()

order_module = module_api.model('OrderModel', {
    "items": fields.List(fields.Nested(module_api.model('nested_item_model', nested_item_model))),
    "payment_amount": fields.Float(exclusiveMin=0.1),
    "order_note": fields.String()
})


class Orders(Resource):

    @validate()
    @module_api.expect(order_module)
    def post(self, body: CreateItemOrderModel):
        """ api to place orders """
        APIResponse()
        _logger.info(f"Creating order")
        try:
            post_data = dict(body)
            item_ids = [x['item_id'] for x in post_data['items']]
            sql_item_ids = ",".join(map(str,item_ids))
            query = f"SELECT id item_id, price p, quantity available from menu where id in ({sql_item_ids})"
            db_rec = db.session.execute(query)
            result = [{'item_id': row.item_id, 'price': row.p, 'available': row.available} for row in db_rec]

            is_valid, msg, merged_rec = self.validate_order(post_data, result)
            if not is_valid and merged_rec is None:
                return return_res(msg, EAPIResponseCode.internal_error)

            is_placed, msg = self.place_order(post_data)
            if not is_placed:
                return return_res(msg, EAPIResponseCode.internal_error)

            order_uid = msg
            _logger.info(f"updating menu for order placed : {order_uid}")
            is_updated, msg = self.update_menu(merged_rec)
            if not is_updated:
                return return_res(msg, EAPIResponseCode.internal_error)

            return return_res(f"Order placed successfully for order id : {order_uid}", EAPIResponseCode.success)

        except Exception as error:
            _logger.error(f"Error while trying to create a order : {error}")
            return return_res(f"Error while trying to create a order ", EAPIResponseCode.internal_error)

    def validate_order(self,post_data, result):
        item_details = post_data['items']
        payment_amount = post_data['payment_amount']

        missing_items = list(set([x['item_id'] for x in item_details]).difference(set([i['item_id'] for i in result])))
        if len(missing_items) > 0:
            _logger.error(f"Item id : {missing_items} does not exist")
            return False, f"Item id : {missing_items} does not exist", None
        merged_result = self.get_merged_dict(result, item_details)

        quantity_available = [(i['item_id'], i['available']) for i in merged_result if i['quantity']>i['available']]

        if len(quantity_available) > 0:
            _logger.error(f"Quantities available for items : {[f'only {x[1]} quantities are available for item id : {x[0]}' for x in quantity_available]}")
            return False, f"Quantities available for items : {[f'only {x[1]} quantities are available for item id : {x[0]}' for x in quantity_available]}", None
        total = sum([i['quantity']*i['price'] for i in merged_result])

        if payment_amount != float(total):
            _logger.error(f"please check the given payment amount")
            return False, f"please check the given payment amount", None
        return True, total, merged_result

    def get_merged_dict(self,result, item_details):
        _logger.info(f"Merge item details with db data")
        df1 = pd.DataFrame(result).set_index('item_id')
        df2 = pd.DataFrame(item_details).set_index('item_id')
        df = df1.merge(df2, left_index=True, right_index=True)
        df.T.to_dict()

        merged_result = [dict({"item_id": i, **df.T.to_dict()[i]}) for i in df.T.to_dict().keys()]
        return merged_result

    @staticmethod
    def place_order(post_data):
        try:
            _logger.info(f"Placing order")
            order_info = OrderModel(**post_data)
            db.session.add(order_info)
            db.session.commit()
            db.session.refresh(order_info)
            order_uid = order_info.id
            _logger.info(f"Order placed successfully for order id : {order_uid}")
            return True, order_uid
        except Exception as error:
            _logger.error(f"Error while creating order : {error}")
            return False, error

    @staticmethod
    def update_menu(merged_rec):
        try:
            updated_menu_rec = [{'id': i['item_id'], 'quantity': i['available'] - i['quantity']} for i in merged_rec]
            db.session.bulk_update_mappings(MenuModel, updated_menu_rec)
            db.session.commit()
            _logger.info(f"Menu has been updated successfully")
            return True, None
        except Exception as error:
            _logger.error(f"Error while updating menu {error}")
            return False, error


class FetchOrders(Resource):
    @validate()
    def get(self, order_id: int):
        """ Fetch order details based on order id """
        APIResponse()
        try:
            order_info = db.session.query(OrderModel).filter_by(id=order_id).first()
            if order_info is None:
                _logger.error(f"No orders found with order id : {order_id}")
                return return_res(f"No orders found with order id :{order_id}",
                                        EAPIResponseCode.no_records)
            del order_info.__dict__['_sa_instance_state']
            order_res= {
                "items": order_info.items,
                "payment_amount": float(order_info.payment_amount),
                "order_note": order_info.order_note,
                "id": order_info.id
            }
            return return_res(order_res, EAPIResponseCode.success)
        except Exception as error:
            _logger.error(f"Error while trying to fetch records for order id : {order_id} : {error}")
            return return_res(f"Error while trying to fetch records for order id ", EAPIResponseCode.internal_error)


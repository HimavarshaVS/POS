from flask_restx import Resource
from flask import request
from flask_pydantic import validate
from commons.service_logger.logger_factory_service import SrvLoggerFactory
from models.api_response import APIResponse, EAPIResponseCode
from models.menu_model import OrderModel, MenuModel
from models.base_models import *
from db import db
import pandas as pd

_API_NAMESPACE = "Orders"
_logger = SrvLoggerFactory(_API_NAMESPACE).get_logger()


class Orders(Resource):

    @validate()
    def post(self, body: CreateItemBaseModel):
        """ api to place orders """
        res = APIResponse()
        _logger.info(f"Creating order")
        try:
            """
            2. validate price for list of items
            """

            post_data = dict(body)
            item_ids = [x['item_id'] for x in post_data['items']]
            query = f"SELECT id item_id, price p, quantity available from menu where id in {tuple(item_ids)}"
            db_rec = db.session.execute(query)
            result = [{'item_id': row.item_id, 'price': row.p, 'available': row.available} for row in db_rec]

            is_valid, msg, merged_rec = self.validate_order(post_data, result)
            if not is_valid and merged_rec is None:
                res.set_result(msg)
                res.set_code(EAPIResponseCode.bad_request)
                return res.response

            _logger.info(f"Placing order")
            order_info = OrderModel(**post_data)
            db.session.add(order_info)
            db.session.commit()
            db.session.refresh(order_info)
            order_uid = order_info.id
            _logger.info(f"Order placed successfully for order id : {order_uid}")

            _logger.info(f"updating menu for order placed : {order_uid}")
            updated_menu_rec = [{'id': i['item_id'], 'quantity':i['available']-i['quantity']} for i in merged_rec]
            db.session.bulk_update_mappings(MenuModel, updated_menu_rec)
            db.session.commit()
            _logger.info(f"Menu has been updated successfully")

            res.set_result(f"Order placed successfully for order id : {order_uid}")
            res.set_code(EAPIResponseCode.success)
            return res.response
        except Exception as error:
            _logger.error(f"Error while trying to create a order : {error}")
            res.set_result(f"Error while trying to create order")
            res.set_code(EAPIResponseCode.internal_error)
            return res.response

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

        if payment_amount != total:
            _logger.error(f"please check the given payment amount")
            return False, f"please check the given payment amount", None
        return True, total, merged_result

    def get_merged_dict(self,result, item_details):

        df1 = pd.DataFrame(result).set_index('item_id')
        df2 = pd.DataFrame(item_details).set_index('item_id')
        df = df1.merge(df2, left_index=True, right_index=True)
        df.T.to_dict()

        merged_result = [dict({"item_id": i, **df.T.to_dict()[i]}) for i in df.T.to_dict().keys()]
        return merged_result

    @validate()
    def get(self, order_id: int):
        res = APIResponse()
        try:
            order_info = db.session.query(OrderModel).filter_by(order_id)
            db_rec = order_info.__dict__
            res.set_result(db_rec)
            res.set_code(EAPIResponseCode.success)
        except Exception as error:
            _logger.error(f"Error while trying to fetch records for order id : {order_id} : {error}")
            res.set_result(f"Error while trying to fetch records for order id : {order_id} : {error}")
            res.set_code(EAPIResponseCode.internal_error)


if __name__ == '__main__':
    om = Orders()
    item_details = [
        {
            "item_id": 22,
            "quantity": 3
        },{
            "item_id": 7,
            "qunatity": 1
        }
    ]
    om.validate_quantity(item_details)
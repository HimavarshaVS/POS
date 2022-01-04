
from pydantic import *
from typing import Optional


class ItemBaseModel(BaseModel):
    description: constr(min_length=3, max_length=30)
    price:  confloat(gt=1)
    quantity: conint()
    modifiers: Optional[dict]
    item_name: constr(min_length=3, max_length=50)


class UpdateItemBaseModel(BaseModel):
    description: Optional[constr(min_length=3, max_length=100)]
    price: Optional[confloat()]
    quantity: Optional[conint()]
    modifiers: Optional[dict]
    item_name: Optional[constr(min_length=3, max_length=50)]


class CreateItemOrderModel(BaseModel):
    items: list
    payment_amount:  confloat(gt=1)
    order_note: Optional[constr(min_length=3, max_length=30)]


order_schema = {
    "type": "object",
    "properties" : {
        "item_id": {"type": "int"},
        "quantity": {"type": "float"},
        "modifiers": {"type": "object"}
    },
    "required": ["item_id", "quantity"]
}
#
#
# def validate_order_schema(payload):
#     try:
#         validate(instance=payload, schema=order_schema)
#         return True
#     except Exception as e:
#         return e.args[0]
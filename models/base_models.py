from pydantic import BaseModel

from pydantic import *
from typing import Optional


class ItemBaseModel(BaseModel):
    description: constr(min_length=3, max_length=6)
    price: confloat()
    quantity: conint()
    modifiers: Optional[dict]
    item_name: constr(min_length=3, max_length=50)


class UpdateItemBaseModel(BaseModel):
    description: Optional[constr(min_length=3, max_length=100)]
    price: Optional[confloat()]
    quantity: Optional[conint()]
    modifiers: Optional[dict]
    item_name: Optional[constr(min_length=3, max_length=50)]


class CreateItemBaseModel(BaseModel):
    items: list
    payment_amount: confloat()
    order_note: Optional[constr()]

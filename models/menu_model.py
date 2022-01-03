from db import db
from sqlalchemy.dialects.postgresql import JSONB

class MenuModel(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80))
    price = db.Column(db.Float())
    quantity = db.Column(db.Integer())
    modifiers = db.Column(db.JSON())
    item_name = db.Column(db.String(), unique=True)


class OrderModel(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_note = db.Column(db.String())
    payment_amount = db.Column(db.Numeric())
    items = db.Column(JSONB)




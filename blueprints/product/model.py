from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from datetime import datetime
from blueprints.client.model import Clients
from blueprints.category.model import Categories
from blueprints.subcategory.model import SubCategories
from sqlalchemy import Integer, String, Column, ForeignKey

class Products(db.Model):

    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_id = db.Column(db.Integer, ForeignKey(Clients.id, ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, ForeignKey(Categories.id, ondelete='CASCADE'), nullable=False)
    subcategory_id = db.Coumn(db.Integer, ForeignKey(SubCategories.id, ondelete='CASCADE'), nullable=False)
    url_image = db.Column(db.String(255))
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    promo = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        'id': fields.Integer,
        'seller_id': fields.Integer,
        'category_id':fields.Integer,
        'subcategory_id':fields.Integer,
        'url_image':fields.String,
        'name': fields.String,
        'price': fields.Integer,
        'stock' : fields.Integer,
        'promo' : fields.String,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
    }

    def __init__(self, seller_id, category_id, subcategory_id, url_image, name, price, stock, promo):
        self.seller_id = seller_id,
        self.category_id = category_id,
        self.subcategory_id = subcategory_id,
        self.url_image = url_image
        self.name = name
        self.price = price
        self.stock = stock
        self.promo = promo

    def __repr__(self): 
        return '<Product %r>' %self.id
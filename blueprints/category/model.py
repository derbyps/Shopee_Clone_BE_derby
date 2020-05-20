from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship


class Categories(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    imgURL = db.Column(db.String(255))
    name = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    product = db.relationship("Products", cascade="all, delete-orphan", passive_deletes=True)
    subcategory = db.relationship("SubCategories", cascade="all, delete-orphan", passive_deletes=True)
    
    response_fields = {
        'id': fields.Integer,
        'imgURL': fields.String,
        'name': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, imgURL, name):
        self.imgURL = imgURL
        self.name = name

    def __repr__(self):
        return '<Categories %r>' % self.id
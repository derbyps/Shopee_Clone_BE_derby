from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship
from blueprints.category.model import Categories
from sqlalchemy import Integer, String, Column, ForeignKey


class SubCategories(db.Model):
    __tablename__ = "subcategory"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category_id = db.Column(db.Integer, ForeignKey(Categories.id, ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    product = db.relationship("Products", cascade="all, delete-orphan", passive_deletes=True)

    response_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'category_id': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id

    def __repr__(self):
        return '<SubCategories %r>' % self.id
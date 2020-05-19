from blueprints import db
from datetime import datetime
from sqlalchemy.sql import func
from flask_restful import fields
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

class Clients(db.Model):
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255))
    salt = db.Column(db.String(255))
    status = db.Column(db.Boolean, nullable=True, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields ={
        'id' : fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'status' : fields.Boolean,
        'created_at' : fields.DateTime,
        'updated_at' : fields.DateTime
        }

    jwt_claims_fields = {
        'id' : fields.Integer,
        'username' : fields.String,
        'status' : fields.Boolean
    }

    def __init__(self, username, password, status, salt):
        self.username = username
        self.password = password
        self.status = status
        self.salt = salt
      
    def __repr__(self):
        return '<Client %r>'%self.id
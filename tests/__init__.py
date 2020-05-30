import pytest 
import logging
import json
import hashlib
import uuid
import os
from sqlalchemy.sql import func
from blueprints import app, cache, db
from flask import Flask, request, json
from blueprints.client.model import Clients
from blueprints.category.model import Categories
from blueprints.product.model import Products
from blueprints.subcategory.model import SubCategories

def call_client(request):
    client = app.test_client()
    return client

@pytest.fixture
def client(request):
    return call_client(request)

@pytest.fixture
def init_database():
    db.drop_all()
    db.create_all()
    
    salt = uuid.uuid4().hex
    encoded = ('%s%s' %("admin", salt)).encode('utf-8')
    hashpass = hashlib.sha512(encoded).hexdigest()
    encoded2 = ('%s%s' %("alta123", salt)).encode('utf-8')
    hashpass2 = hashlib.sha512(encoded2).hexdigest()
    client_internal = Clients(username='admin', password=hashpass, salt=salt, status=True)
    client_noninternal = Clients(username='derby', password=hashpass2, salt=salt, status=False)    
    db.session.add(client_internal)
    db.session.add(client_noninternal)
    
    db.session.commit()
    
    category = Categories(imgURL="google.com", name='Makanan')
    db.session.add(category)
    db.session.commit()
    
    subcategory = SubCategories(name="makanan", category_id=1)
    db.session.add(subcategory)
    db.session.commit()
    
    product = Products(seller_id=1, category_id=1, subcategory_id=1, url_image="google.com", name="makan", price=10, stock=12, promo="Ya")
    db.session.add(product)
    db.session.commit()
    
    
    yield db
    
    db.drop_all()
    
    
def create_token():
    token = cache.get('test-token')
    if token is None:
        data={
            'username': 'admin',
            'password': 'admin'
        }
    
        req = call_client(request)
        res = req.get('/auth', query_string=data)
        
        res_json = json.loads(res.data)
        
        logging.warning('RESULT : %s', res_json)
        
        assert res.status_code == 200
        
        cache.set('test-token', res_json['token'], timeout=60)
        
        return res_json['token']
    else:
        return token

# @pytest.fixture
def test_production():
    return os.environ['Production']

def create_token_non_internal():
    token = cache.get('test-token-non-internal')
    if token is None:
        data={
            'username': 'derby',
            'password': 'alta123'
        }
    
        req = call_client(request)
        res = req.get('/auth', query_string=data)
        
        res_json = json.loads(res.data)
        
        logging.warning('RESULT : %s', res_json)
        
        assert res.status_code == 200
        
        cache.set('test-token-non-internal', res_json['token'], timeout=60)
        
        return res_json['token']
    else:
        return token
from flask import Flask, request
import json, logging
from datetime import datetime
from sqlalchemy import desc
from flask_restful import Resource, Api, reqparse, marshal
from logging.handlers import RotatingFileHandler
from flask import Blueprint
from blueprints.client.model import Clients
from .model import Products
from blueprints import app, db
from blueprints.category.model import Categories
from flask_jwt_extended import jwt_required, get_jwt_claims
import werkzeug, requests


bp_product= Blueprint('product',__name__)
api = Api(bp_product)

class ProductResources(Resource):
    # @jwt_required
    def get(self, id):
        qry = Products.query.get(id)
        if qry is not None:
            QRY = marshal(qry, Products.response_fields)
            cat = Categories.query.filter_by(
                id=QRY['category_id']).first()
            QRY["cat_detail"] = marshal(cat, Categories.response_fields) 
            return QRY, 200
        return {'status': 'NOT_FOUND'}, 404
    
    def postImage(self, imgFile) :
        url = app.config['IMG_URL']
        clientID = app.config['IMG_CLIENT_ID']
        
        payload = {}
        files = [
        ('image', imgFile)
        ]
        ncid = 'Client-ID ' + clientID
        headers = {
        'Authorization': ncid
        }

        res = requests.post(url, headers=headers, data = payload, files = files)
        response = res.json()

        link = response['data']['link']

        return link
    
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url_image', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('name', location='form', required=True)
        parser.add_argument('price', location='form', required=True)
        parser.add_argument('stock', location='form')
        parser.add_argument('promo', location='form')
        parser.add_argument('category_id', location='form')
        parser.add_argument('subcategory_id', location='form')
        args = parser.parse_args()
        
        image_product = args['url_image']
        
        if image_product :
            img_link = self.postImage(image_product)

        claims = get_jwt_claims()
        qry = Clients.query.filter_by(id=claims["id"]).first()
        seller_id = qry.id

        product = Products(seller_id, args["category_id"], args["subcategory_id"], img_link, args['name'], args['price'], args['stock'], args['promo'])
        db.session.add(product)
        db.session.commit()
        app.logger.debug('DEBUG: %s', product)
        
        return marshal(product, Products.response_fields), 200, {'Content-Type': 'application/json'}

class ProductList(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('name', location='args')
        parser.add_argument('size', location='args')
        parser.add_argument('price', location='args')
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('name', 'size', 'price'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']
        qry = Products.query

        if args['name'] is not None:
            qry = qry.filter_by(name=args['name'])

        if args['price'] is not None:
            qry = qry.filter_by(price=args['price'])

        if args['orderby'] is not None:
            if args['orderby'] == 'name':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Products.name))
                else:
                    qry = qry.order_by(Products.name)
            elif args['orderby'] == 'price':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Products.price))
                else:
                    qry = qry.order_by(Products.price)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            QRY = marshal(row, Products.response_fields)
            cat = Categories.query.filter_by(id=QRY['category_id']).first()
            QRY["cat_detail"] = marshal(cat, Categories.response_fields)
            rows.append(QRY)

        return rows, 200
    
api.add_resource(ProductResources,'','/<id>')
api.add_resource(ProductList, '', '/list')
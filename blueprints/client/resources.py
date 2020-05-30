import json
import uuid, hashlib
from .model import Clients
from sqlalchemy import desc
from blueprints import db, app
from flask import Blueprint, Flask
from blueprints import internal_required
from flask_restful import Api, reqparse, Resource, marshal

bp_client = Blueprint('client', __name__)
api = Api(bp_client)

class ClientResource(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json')
        parser.add_argument('status',type=bool, location='json')
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        client = Clients(args['username'], hash_pass, args['status'], salt)
        db.session.add(client)
        db.session.commit()

        app.logger.debug('DEBUG: %s', client)

        return marshal(client, Clients.response_fields), 200

    @internal_required
    def get(self,id=None):
        qry = Clients.query.get(id)

        if qry is not None:
            return marshal(qry,Clients.response_fields), 200, {
            'Content-Type':'application/json'
            }
        return {'Status':'id is gone'}, 404, {'Content-Type':'application/json'}

    @internal_required  
    def patch(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json')
        parser.add_argument('password', location='json')
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        qry = Clients.query.get(id)
        if qry is None:
            return {'Status ': 'Not Found'}, 404
        
        qry.username = args['username']
        qry.password = hash_pass
        qry.salt = salt
        db.session.commit()

        return marshal(qry, Clients.response_fields), 200

    @internal_required        
    def delete(self,id=None):
        if id is not None:
            qry = Clients.query.get(id)
            if qry is not None:
                db.session.delete(qry)
                db.session.commit()
                return 'Data telah terhapus', 200, {
                'Content-Type':'application/json'
                }
            else:
                return 'id is not found', 404, {
                'Content-Type':'application/json'
                }
        
class ClientList(Resource):
    
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        
        args = parser.parse_args()
        offset = (args['p']*args['rp']-args['rp'])
        qry = Clients.query    

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Clients.response_fields))
        
        return rows,200
    
api.add_resource(ClientList, '', '/list')
api.add_resource(ClientResource, '', '/<id>')
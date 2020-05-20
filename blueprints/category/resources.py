import json
import werkzeug, requests
from sqlalchemy import desc
from .model import Categories
from blueprints import db, app
from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
# from blueprints import internal_required

bp_category = Blueprint('category', __name__)
api = Api(bp_category)


class CategoryResource(Resource):

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


    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('imgURL', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('name', location='form', required=True)

        args = parser.parse_args()
        
        image_category = args['imgURL']
        
        if image_category :
            img_link = self.postImage(image_category)
        
        category = Categories(img_link, args['name'])
        db.session.add(category)
        db.session.commit()

        app.logger.debug('DEBUG: %s', category)

        return marshal(category, Categories.response_fields), 200

    def get(self, id):
        qry = Categories.query.get(id)

        if qry is not None:
            return marshal(qry, Categories.response_fields), 200, {
                'Content-Type': 'application/json'
            }
        return {'Status': 'Not Found'}, 404, {'Content-Type': 'application/json'}

    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        args = parser.parse_args()

        qry = Categories.query.get(id)
        if qry is None:
            return {'Status ': 'Not Found'}, 404

        qry.username = args['name']
        db.session.commit()

        return marshal(qry, Categories.response_fields), 200

    def delete(self, id):

        qry = Categories.query.get(id)
        if qry is None:
            return {'status': 'Not Found'}, 404
        db.session.delete(qry)
        db.session.commit()

        return {'status': "Deleted"}, 200


class CategoryList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        args = parser.parse_args()

        offset = (args['p']*args['rp']-args['rp'])
        qry = Categories.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Categories.response_fields))

        return rows, 200


api.add_resource(CategoryList, '', '/list')
api.add_resource(CategoryResource, '', '/<id>')
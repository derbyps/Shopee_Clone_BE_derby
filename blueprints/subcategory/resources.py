import json
import werkzeug, requests
from sqlalchemy import desc
from .model import SubCategories
from blueprints import db, app
from flask import Blueprint, Flask
from flask_restful import Api, reqparse, Resource, marshal
# from blueprints import internal_required

bp_subcategory = Blueprint('subcategory', __name__)
api = Api(bp_subcategory)


class SubCategoryResource(Resource):

    # @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('category_id', location='json', required=True)

        args = parser.parse_args()
        
        subcategory = SubCategories(args['name'], args['category_id'])
        db.session.add(subcategory)
        db.session.commit()

        app.logger.debug('DEBUG: %s', subcategory)

        return marshal(subcategory, SubCategories.response_fields), 200

    def get(self, id):
        qry = SubCategories.query.get(id)

        if qry is not None:
            return marshal(qry, SubCategories.response_fields), 200, {
                'Content-Type': 'application/json'
            }
        return {'Status': 'Not Found'}, 404, {'Content-Type': 'application/json'}

    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json')
        parser.add_argument('category_id', location='json')
        args = parser.parse_args()

        qry = SubCategories.query.get(id)
        if qry is None:
            return {'Status ': 'Not Found'}, 404

        qry.name = args['name']
        qry.category_id = args['category_id']
        db.session.commit()

        return marshal(qry, SubCategories.response_fields), 200

    def delete(self, id):

        qry = SubCategories.query.get(id)
        if qry is None:
            return {'status': 'Not Found'}, 404
        db.session.delete(qry)
        db.session.commit()

        return {'status': "Deleted"}, 200


class SubCategoryList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        args = parser.parse_args()

        offset = (args['p']*args['rp']-args['rp'])
        qry = SubCategories.query

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, SubCategories.response_fields))

        return rows, 200


api.add_resource(SubCategoryList, '', '/list')
api.add_resource(SubCategoryResource, '', '/<id>')
__author__ = 'srininara'

from flask.ext.restful import Resource
from app import api
import app.service.service_category as cat_sv


class CategoryListAPI(Resource):
    def get(self):
        return {"categories": cat_sv.get_cat_sub_cat_listing()}, 200

api.add_resource(CategoryListAPI, '/grihasthi/api/v1.0/categories', endpoint='categories')


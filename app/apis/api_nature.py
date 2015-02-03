__author__ = 'srininara'

from flask.ext.restful import Resource
from app import api
import app.service.service_nature as nat_sv


class NatureListAPI(Resource):
    def get(self):
        return {"natures": nat_sv.get_nat_listing()}, 200

api.add_resource(NatureListAPI, '/grihasthi/api/v1.0/natures', endpoint='natures')


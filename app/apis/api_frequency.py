__author__ = 'srininara'

from flask.ext.restful import Resource
from app import api
import app.service.service_frequency as freq_sv


class FrequencyListAPI(Resource):
    def get(self):
        return {"frequencies": freq_sv.get_freq_listing()}, 200

api.add_resource(FrequencyListAPI, '/grihasthi/api/v1.0/frequencies', endpoint='frequencies')


__author__ = 'srininara'

from flask.ext.restful import Resource
from app import api
import app.month_stats_provider as msp


class MonthStatsDailyAPI(Resource):
    def get(self, month_identifier):
        output = {}
        output["dailyData"], output["summary"] = msp.dailyData(month_identifier)
        return output, 200


class MonthStatsCategoryAPI(Resource):
    def get(self, month_identifier):
        output = {"categoryData": msp.categoryData(month_identifier)}
        return output, 200


api.add_resource(MonthStatsCategoryAPI, '/grihasthi/api/v1.0/monthStatsCategory/<string:month_identifier>',
                 endpoint='monthStatsCategory')
api.add_resource(MonthStatsDailyAPI, '/grihasthi/api/v1.0/monthStatsDaily/<string:month_identifier>',
                 endpoint='monthStatsDaily')
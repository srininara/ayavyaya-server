__author__ = 'srininara'

from flask.ext.restful import Resource
from app import api
import app.month_stats_provider as msp


class MonthStatsDailyAPI(Resource):
    def get(self, month_identifier):
        # Behavior note: Even when data for the criteria is not found, the stats api returns 200 with empty shells
        output = {}
        output["dailyData"], output["summary"], output["prev_month_summary"], output["comparison"] = msp.daily_stats(
            month_identifier)
        return output, 200


class MonthStatsCategoryAPI(Resource):
    def get(self, month_identifier):
        # Behavior note: Even when data for the criteria is not found, the stats api returns 200 with empty shells
        output = {"categoryData": msp.category_stats(month_identifier)}
        return output, 200


class MonthStatsTopExpensesAPI(Resource):
    def get(self, month_identifier):
        # Behavior note: Even when data for the criteria is not found, the stats api returns 200 with empty shells
        output = {}
        output["topExpensesByValue"], output["topExpensesByFrequency"] = msp.top_expenses_stats(month_identifier)
        return output, 200


api.add_resource(MonthStatsCategoryAPI, '/grihasthi/api/v1.0/monthStatsCategory/<string:month_identifier>',
                 endpoint='monthStatsCategory')
api.add_resource(MonthStatsDailyAPI, '/grihasthi/api/v1.0/monthStatsDaily/<string:month_identifier>',
                 endpoint='monthStatsDaily')
api.add_resource(MonthStatsTopExpensesAPI, '/grihasthi/api/v1.0/monthStatsTopExpenses/<string:month_identifier>',
                 endpoint='monthStatsTopExpenses')
from flask.ext.restful import Resource
from ayavyaya import api
import ayavyaya.service.month_stats_provider as msp


class MonthStatsDailyAPI(Resource):
    def get(self, month_identifier):
        # Behavior note: Even when data for the criteria is not found, the stats apis returns 200 with empty shells
        output_arr = msp.daily_stats(month_identifier)

        output = {"dailyData": output_arr[0], "summary": output_arr[1], "prev_month_summary": output_arr[2],
                  "comparison": output_arr[3]}
        return output, 200


class MonthStatsCategoryAPI(Resource):
    def get(self, month_identifier):
        # Behavior note: Even when data for the criteria is not found, the stats apis returns 200 with empty shells
        output = {"categoryData": msp.category_stats(month_identifier)}
        return output, 200


class MonthStatsTopExpensesAPI(Resource):
    def get(self, month_identifier):
        # Behavior note: Even when data for the criteria is not found, the stats apis returns 200 with empty shells
        output_arr = msp.top_expenses_stats(month_identifier)
        output = dict(topExpensesByValue=output_arr[0], topExpensesByFrequency=output_arr[1])
        return output, 200


api.add_resource(MonthStatsCategoryAPI, '/ayavyaya/api/v1.0/monthStatsCategory/<string:month_identifier>',
                 endpoint='monthStatsCategory')
api.add_resource(MonthStatsDailyAPI, '/ayavyaya/api/v1.0/monthStatsDaily/<string:month_identifier>',
                 endpoint='monthStatsDaily')
api.add_resource(MonthStatsTopExpensesAPI, '/ayavyaya/api/v1.0/monthStatsTopExpenses/<string:month_identifier>',
                 endpoint='monthStatsTopExpenses')

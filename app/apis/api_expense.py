from flask import request

from flask.ext.restful import Resource, reqparse
from app import api
from app import app


import app.service.service_expense as ex_sv

log = app.logger


class ExpenseListAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('index', type=int)
        parser.add_argument('size', type=int)
        args = parser.parse_args()
        index = args.get("index")
        size = args.get("size")
        try:
            expenses = ex_sv.get_expenses(index, size)
            return {"expenses": expenses}, 200
        except ValueError as v:
            return {"error": v.message}, 400

    def post(self):
        try:
            log.debug("Expense Post Called ")
            expense_out = ex_sv.add_expense(request.json)
            expense_out['amount'] = str(expense_out['amount'])
            return expense_out, 201
        except ValueError as err:
            err_out = {}
            err_out['message'] = err.message
            return err_out, 400

class ExpenseAPI(Resource):
    def get(self, id):
        print("expense get")

    def put(self, id):
        try:
            log.debug("Expense Put Called")
            expense_updated = ex_sv.update_expense(id, request.json)
            return expense_updated, 200
        except ValueError as err:
            err_out = {}
            err_out['message'] = err.message
            return err_out, 400

    def delete(self, id):
        print("expense delete")


class ExpenseAggregatesAPI(Resource):
    def get(self, period):
        summary_key = period + "Summary"
        output, summaries = ex_sv.get_expense_aggregates(period)
        return {period: output, summary_key: summaries}, 200


class ClassifiedExpensesAPI(Resource):
    def get(self, classificationType):
        split = request.args.get('split')
        if split:
            print(split)
            output = ex_sv.get_expense_aggregates_for_classification_with_split(classificationType, split)
        else:
            print(split)
            output = ex_sv.get_expense_aggregates_for_classification(classificationType)
        return {classificationType: output}, 200

api.add_resource(ExpenseListAPI, '/grihasthi/api/v1.0/expenses', endpoint='expenses')
api.add_resource(ExpenseAPI, '/grihasthi/api/v1.0/expenses/<int:id>', endpoint='expense')
api.add_resource(ExpenseAggregatesAPI, '/grihasthi/api/v1.0/expenseAggregates/<string:period>',
                 endpoint='expenseAggregates')
api.add_resource(ClassifiedExpensesAPI, '/grihasthi/api/v1.0/expenseClassification/<string:classificationType>',
                 endpoint='expenseClassification')

from flask import request

from flask.ext.restful import Resource  # , reqparse
from app import api
import app.service_expense as ex_sv


class ExpenseListAPI(Resource):
    def get(self):
        print("expenses list get")

    def post(self):
        expense_out = ex_sv.add_expense(request.json)
        return expense_out, 201


class ExpenseAPI(Resource):
    def get(self, id):
        print("expense get")

    def put(self, id):
        print("expense put")

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

# class NatureOfExpenseAPI(Resource):
# def get(self):
#     return {"nature": ex_sv.get_expense_aggregates_for_nature_with_split()}

api.add_resource(ExpenseListAPI, '/grihasthi/api/v1.0/expenses', endpoint='expenses')
api.add_resource(ExpenseAPI, '/grihasthi/api/v1.0/expenses/<int:id>', endpoint='expense')
api.add_resource(ExpenseAggregatesAPI, '/grihasthi/api/v1.0/expenseAggregates/<string:period>',
                 endpoint='expenseAggregates')
api.add_resource(ClassifiedExpensesAPI, '/grihasthi/api/v1.0/expenseClassification/<string:classificationType>',
                 endpoint='expenseClassification')
# api.add_resource(NatureOfExpenseAPI, '/grihasthi/api/v1.0/expenseNature', endpoint='expenseNature')

from flask.ext.restful import Resource#, reqparse
from flask import request
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
    output = ex_sv.get_expense_aggregates(period)
    print(output)
    return {period:output}, 200


api.add_resource(ExpenseListAPI, '/grihasthi/api/v1.0/expenses', endpoint = 'expenses')
api.add_resource(ExpenseAPI, '/grihasthi/api/v1.0/expenses/<int:id>', endpoint = 'expense')
api.add_resource(ExpenseAggregatesAPI, '/grihasthi/api/v1.0/expenseAggregates/<string:period>', endpoint = 'expenseAggregates')

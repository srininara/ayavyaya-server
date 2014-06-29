import json
from flask.ext.restful import Resource, reqparse
from flask import request
from app import api
from app import db
from app.model_expense import Expense
from app.model_expense import expense_from_dict
from app.api_inputs import to_date

class ExpenseListAPI(Resource):
  def __init__(self):
    self.reqparse = reqparse.RequestParser()
    self.reqparse.add_argument('description', type=str, default='', location='json')
    self.reqparse.add_argument('expense_date', type=to_date, location='json')
    self.reqparse.add_argument('amount', type=float, default='', location='json')
    super(ExpenseListAPI,self).__init__()

  def get(self):
    print("expenses list get")

  def post(self):
    # print(request.json)
    expense = expense_from_dict(request.json)

    # # print(json.loads(request.json,object_hook=expense_from_dict))
    # print("-------------------")
    #
    # args = self.reqparse.parse_args()
    # print(args)
    # expense = Expense(args.description, args.expense_date, args.amount)
    db.session.add(expense)
    db.session.commit()
    return '',201

class ExpenseAPI(Resource):
  def get(self, id):
    print("expense get")

  def put(self, id):
    print("expense put")

  def delete(self, id):
    print("expense delete")

api.add_resource(ExpenseListAPI, '/grihasthi/api/v1.0/expenses', endpoint = 'expenses')
api.add_resource(ExpenseAPI, '/grihasthi/api/v1.0/expenses/<int:id>', endpoint = 'expense')

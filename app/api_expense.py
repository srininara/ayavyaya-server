from flask.ext.restful import Resource#, reqparse
from flask import request
from app import api
from app import db
from app.model_expense import Expense
from app.model_expense import expense_from_dict
from app.model_tag import Tag
from app.model_tag import tag_from_dict
from app.api_inputs import to_date
from app.model_expense import to_dict

class ExpenseListAPI(Resource):

  def get(self):
    print("expenses list get")

  def post(self):
    expense = expense_from_dict(request.json)
    tags_data = request.json.get('tags',None)

    if tags_data is not None:
      for tag_data in tags_data:
        tag = tag_from_dict(tag_data)
        if tag is not None:
          expense.add_tag(tag)
    db.session.add(expense)
    db.session.commit()
    return to_dict(expense),201

class ExpenseAPI(Resource):
  def get(self, id):
    print("expense get")

  def put(self, id):
    print("expense put")

  def delete(self, id):
    print("expense delete")

api.add_resource(ExpenseListAPI, '/grihasthi/api/v1.0/expenses', endpoint = 'expenses')
api.add_resource(ExpenseAPI, '/grihasthi/api/v1.0/expenses/<int:id>', endpoint = 'expense')

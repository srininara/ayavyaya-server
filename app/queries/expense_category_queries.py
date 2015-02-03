from app import db
from app.model.model_expense_category import Expense_Category
from app.model.model_expense_subcategory import Expense_Subcategory

def get_cat_sub_cat_listing():
    return db.session.query(Expense_Category.name.label("category"),
                            Expense_Subcategory.name.label("sub_category")).join(
        Expense_Subcategory,
        Expense_Subcategory.category_id == Expense_Category.id).all()

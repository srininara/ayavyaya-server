from app import db
from app.model.model_expense_category import Expense_Category
from app.model.model_expense_subcategory import Expense_Subcategory


def get_cat_sub_cat_listing():
    return db.session.query(Expense_Category.id.label("cat_id"),
                            Expense_Category.name.label("category"),
                            Expense_Category.description.label("cat_desc"),
                            Expense_Subcategory.id.label("subcat_id"),
                            Expense_Subcategory.name.label("sub_category"),
                            Expense_Subcategory.description.label("subcat_desc")).join(
        Expense_Subcategory,
        Expense_Subcategory.category_id == Expense_Category.id).all()

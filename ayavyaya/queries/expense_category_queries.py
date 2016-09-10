from ayavyaya import db
from ayavyaya.model.model_expense_category import ExpenseCategory
from ayavyaya.model.model_expense_subcategory import ExpenseSubcategory


def get_cat_sub_cat_listing():
    return db.session.query(ExpenseCategory.id.label("cat_id"),
                            ExpenseCategory.name.label("category"),
                            ExpenseCategory.description.label("cat_desc"),
                            ExpenseSubcategory.id.label("subcat_id"),
                            ExpenseSubcategory.name.label("sub_category"),
                            ExpenseSubcategory.description.label("subcat_desc")).join(
        ExpenseSubcategory,
        ExpenseSubcategory.category_id == ExpenseCategory.id).all()

""" Will hold the tag model and also the many to many table connecting it to expense """
from ayavyaya import db

tags = db.Table('expenses_tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('expense_id', db.Integer, db.ForeignKey('expense.id')),
                )


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))

    def __init__(self, name):
        self.name = name


def to_dict(tag):
    out = {'id': tag.id, 'name': tag.name}
    return out


def tag_from_dict(the_dict):
    tag_id = the_dict.get('id', -1)
    name = the_dict.get('name', "")
    if tag_id != -1:
        tag = Tag.query.get(tag_id)
        return tag
    elif name != "":
        tag = Tag.query.filter_by(name=name).first()
        if tag is None:
            tag = Tag(name)
        return tag
    else:
        return None

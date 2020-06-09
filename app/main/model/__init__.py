from .. import db


class Identity(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Named(db.Model):
    __abstract__ = True
    name = db.Column(db.String(128), nullable=False, unique=True)
    code = db.Column(db.String(512), nullable=True)


class Audit(db.Model):
    __abstract__ = True
    created_by = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String(128))
    modified_on = db.Column(db.DateTime)

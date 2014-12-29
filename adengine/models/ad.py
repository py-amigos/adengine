__author__ = 'jkf'

# std
from datetime import datetime

# local
from .core import Base, db


class Ad(Base):
    __tablename__ = 'ads'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # TODO: make it possible to reference author from the Ad also
    # solve cyclic problem
    # author = db.relationship('User', foreign_keys=author_id)

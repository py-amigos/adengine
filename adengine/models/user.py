# encoding: utf-8

# std
from datetime import datetime

# local
from .core import Base
from adengine.app import db


class User(Base):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64), nullable=True)
    about_me = db.Column(db.Text(), nullable=True)

    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    ads = db.relationship('Ad', order_by="Ad.id", backref='author')

    def __str__(self):
        return "User(id={self.id}, username={self.username})".format(self=self)

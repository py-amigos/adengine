# encoding: utf-8

from datetime import datetime

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base


format_time = (lambda data: data.isoformat()
               if isinstance(data, datetime)
               else data)


class BaseModel(object):

    def as_dict(self):
        return {
            c.name: format_time(getattr(self, c.name))
            for c in self.__table__.columns
        }


db = SQLAlchemy()


Base = declarative_base(
    metadata=db.Model.metadata,
    cls=(BaseModel, db.Model))


class Ad(Base):
    __tablename__ = 'ads'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Comment(Base):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ad_id = db.Column(db.Integer, db.ForeignKey('ads.id'))
    ad = db.relationship('Ad', backref=db.backref('comments', order_by=timestamp))
    user = db.relationship('User', backref=db.backref('comments', order_by=timestamp))


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

__author__ = 'jkf'

# std
from datetime import datetime

# local
from .core import Base, db


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

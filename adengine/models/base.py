# from datetime import datetime
#
# from adengine.app import db
#
#
# class Ad(db.Model):
#     __tablename__ = 'ads'
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.Text)
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     comments = db.relationship('Comment', backref='ad', lazy='dynamic')
#
#
# class Comment(db.Model):
#     __tablename__ = 'comments'
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(64), nullable=False)
#     timestamp = db.Column(db.DateTime, index=True,
#                                       default=datetime.utcnow)
#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     ad_id = db.Column(db.Integer, db.ForeignKey('ads.id'), nullable=True)
#     comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'),
#                            nullable=True)
#
#

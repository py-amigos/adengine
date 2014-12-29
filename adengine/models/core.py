# encoding: utf-8

# std
from datetime import datetime

# local
from adengine.app import db

# 3rd-party
from sqlalchemy.ext.declarative import declarative_base


format_time = lambda data: data.isoformat() if isinstance(data, datetime) else data


class BaseModel(object):

    def as_dict(self):
        return {
            c.name: format_time(getattr(self, c.name))
            for c in self.__table__.columns
        }


Base = declarative_base(
    metadata=db.Model.metadata,
    cls=(BaseModel, db.Model))

import os
import pytest

from adengine.app import create_app, configure_endpoints
from adengine.model import db as _db
from adengine.config import TestingConfig

db_path = TestingConfig.DATABASE_PATH


@pytest.yield_fixture
def app():
    app = create_app('testing')
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.yield_fixture
def client(app):
    yield app.test_client()


@pytest.yield_fixture
def db(app):
    if os.path.exists(db_path):
        os.remove(db_path)
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()
    os.remove(db_path)


class SessionWrapper:
    """Helper wrapper to implement auto-removal of added resources.

    Auth removal should happen on each test-case.
    On-add it remembers the resource on explicit call of :meth:`remove_added`
         remove remembered resource from the database.
    """

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.__to_rollback = []

    def __getattr__(self, name):
        return getattr(self.wrapped, name)

    def add(self, resource):
        self.__to_rollback.append(resource)
        return self.wrapped.add(resource)

    def remove_added(self):
        for resource in self.__to_rollback:
            if resource.id:
                self.wrapped.delete(resource)
        self.wrapped.commit()


@pytest.yield_fixture
def session(db, app):
    # from sqlalchemy.orm import sessionmaker, scoped_session

    # Session = sessionmaker(autocommit=False, autoflush=False, bind=db.engine)
    # session = scoped_session(Session)

    session = db.create_scoped_session()

    configure_endpoints(app, session=session, db=db)

    yield session

    session.remove()

import os
import pytest

from adengine.app import create_app
from adengine.model import db as _db
from adengine.config import TestingConfig

db_path = TestingConfig.DATABASE_PATH


@pytest.yield_fixture(scope='session')
def app():
    app = create_app('testing')
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    yield app.test_client()


@pytest.yield_fixture(scope='session')
def db(app):
    if os.path.exists(db_path):
        os.remove(db_path)
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()
    os.remove(db_path)


@pytest.yield_fixture(scope='function')
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    session = db.create_scoped_session()

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()

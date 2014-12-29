import os
basedir = os.path.abspath(os.path.curdir)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    ADENGINE_MAIL_SUBJECT_PREFIX = '[Adengine]'
    ADENGINE_MAIL_SENDER = 'Adengine Admin <adengine@example.com>'
    ADENGINE_ADMIN = os.environ.get('ADENGINE_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DEV_DATABASE_URL')
        or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    )


class TestingConfig(Config):
    TESTING = True
    DATABASE_PATH = os.path.join(basedir, 'data-test.sqlite')
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('TEST_DATABASE_URL')
        or 'sqlite:///' + DATABASE_PATH
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL')
        or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    )


get_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}.get

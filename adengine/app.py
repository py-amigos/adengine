__author__ = "signalpillar"


import adengine.config as app_config

from flask import (
    Flask,
    jsonify,
    make_response,)


from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.errorhandler(404)(not_found)

    config = app_config.get_by_name(config_name)

    app.config.from_object(config)
    config.init_app(app)

    db.init_app(app)
    from flask.ext.restful import Api
    api = Api(app)
    from adengine.views import user
    api.add_resource(user.User, "/api/v1.0/users/<string:user_id>")
    api.add_resource(user.Users, "/api/v1.0/users")
    return app


def not_found(error):
    return make_response(jsonify({
        "error": "Not found"
    }), 404)

import uuid

from adengine.models import user as user_model
from adengine.app import db

from flask.ext.restful import reqparse, Resource, abort


class Users(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)

    def get(self):
        """
        :rtype: list[dict]
        """
        return map(user_model.User.as_dict, user_model.User.query.all())

    def post(self):
        args = self.parser.parse_args()
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "email": args.get('email')
        }
        raise NotImplementedError()
        return user, 201


class User(Resource):

    def get(self, user_id):
        user = user_model.User.query.filter(user_model.User.id == user_id).first()
        return user.as_dict() if user else {}

    def delete(self, user_id):
        user = user_model.User.query.filter_by(id=user_id).first()
        if not user:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        return user.as_dict(), 201

    def put(user_id):
        user = db.User.query.filter_by(id=user_id).first()
        if not user:
            abort(404)
        elif (not request.json
              or 'email' not in request.json):
            abort(400)
        user['email'] = request.json
        return {
            user_id: user
        }

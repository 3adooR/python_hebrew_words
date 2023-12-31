import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from src import db, app
from src.database.models import User
from src.schemas.users import UserSchema


class AuthRegister(Resource):
    user_schema = UserSchema()

    def post(self):
        try:
            user = self.user_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}

        try:
            db.session.add(user)
            db.session.commit()

        except IntegrityError as e:
            db.session.rollback()
            return {'message': str(e)}, 409

        return self.user_schema.dump(user), 201


class AuthLogin(Resource):
    def get(self):
        auth = request.authorization

        if not auth:
            return 'No auth', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}

        user = User.find_user_by_username(auth.get('username', ''))

        if not user or not check_password_hash(user.password, auth.get('password', '')):
            return 'Check password failed', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}

        token = jwt.encode(
            {
                "user_id": user.uuid,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
            },
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        return jsonify({
            "token": token
        })


def token_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        token = request.headers.get('X-API-KEY', '')

        if not token:
            return '', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}

        try:
            uuid = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])['user_id']
        except (KeyError, jwt.ExpiredSignatureError):
            return '', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}

        user = User.find_user_by_uuid(uuid)

        if not user:
            return '', 401, {"WWW-Authenticate": "Basic realm='Authentication required'"}

        return func(self, *args, **kwargs)

    return wrapper

from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from flask import make_response, render_template
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
import traceback
from requests import post
from blacklist import BLACKLIST
from models.user import UserModel


attributes = reqparse.RequestParser()
attributes.add_argument('login', type=str, required=True, help="The 'login' field cannot be empty.")
attributes.add_argument('email', type=str)
attributes.add_argument('password', type=str, required=True, help="The 'password' field cannot be empty.")
attributes.add_argument('confirmed', type=bool)

class User(Resource):
    def get(self, userId):
        user = UserModel.find_user(userId)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    @jwt_required
    def delete(self, userId):
        user = UserModel.find_user(userId)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error occurred while trying to delete the user.'}, 500
            return {'message': 'User deleted.'}, 200
        return {'message': 'User not found.'}, 404

class UserRegister(Resource):
    def post(self):
        data = attributes.parse_args()
        if not data.get('email') or data.get('email') is None:
            return {"message": "The 'email' field cannot be empty."}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": "The email '{}' already exists.".format(data['email'])}, 400

        if UserModel.find_by_login(data['login']):
            return {"message": "The login '{}' already exists.".format(data['login'])}
        
        user = UserModel(**data)
        user.confirmed = False
        try:
            user.save_user()
            user.send_confirmation_email()
        except:
            user.delete_user()
            traceback.print_exc()
            return {'message': 'An internal error has occurred.'}, 500
        return {'message': 'User created successfully!'}, 201

class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = attributes.parse_args()
        user = UserModel.find_by_login(data['login'])

        if user and safe_str_cmp(user.password, data['password']):
            if user.confirmed:
                token = create_access_token(identity=user.userId)
                return {'access_token': token}, 200
            return {'message': 'User not confirmed.'}, 400
        return {'message': 'Incorrect login or password!'}, 401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200

class UserConfirmed(Resource):
    @classmethod
    def get(cls, userId):
        user = UserModel.find_user(userId)
    
        if not user:
            return None
        
        user.confirmed = True
        user.save_user()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user_confirm.html', email=user.email, login=user.login), 200)


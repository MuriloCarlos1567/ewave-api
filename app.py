from flask import Flask, jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from flask_jwt_extended import JWTManager
from resources.product import Products, Product
from resources.user import User, UserRegister, UserLogin, UserLogout, UserConfirmed

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'asdoiwqejasdaskdjoasdj'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_db():
    db.create_all()

@jwt.token_in_blacklist_loader
def blacklist_check(token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def invalid_access_token():
    return jsonify({'message': 'You have been logged out.'}), 401

api.add_resource(Products, '/api/v1/products')
api.add_resource(Product, '/api/v1/products/<string:productId>')
api.add_resource(User, '/api/v1/users/<int:userId>')
api.add_resource(UserRegister, '/api/v1/register')
api.add_resource(UserLogin, '/api/v1/login')
api.add_resource(UserLogout, '/api/v1/logout')
api.add_resource(UserConfirmed, '/api/v1/confirm/<int:userId>')

if __name__ == '__main__':
    from sql_alchemy import db
    db.init_app(app)
    app.run(debug=True)
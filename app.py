from flask import Flask
from flask_restful import Api
from resources.product import Products, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def create_db():
    db.create_all()

api.add_resource(Products, '/api/v1/products')
api.add_resource(Product, '/api/v1/products/<string:productId>')

if __name__ == '__main__':
    from sql_alchemy import db
    db.init_app(app)
    app.run(debug=True)
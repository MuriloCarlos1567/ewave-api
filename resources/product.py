from flask_restful import Resource, reqparse
from models.product import ProductModel
from flask_jwt_extended import jwt_required
import sqlite3

def normalize_path_params(productName=None, category=None, minPrice=0, maxPrice=10000, limit=50, offset=0, **data):
    if category:
        return {
            'minPrice': minPrice,
            'maxPrice': maxPrice,
            'category': category,
            'limit': limit,
            'offset': offset
        }
    return {
            'minPrice': minPrice,
            'maxPrice': maxPrice,
            'limit': limit,
            'offset': offset
        }

path_params = reqparse.RequestParser()
path_params.add_argument('productName', type=str)
path_params.add_argument('category', type=str)
path_params.add_argument('minPrice', type=float)
path_params.add_argument('maxPrice', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)

class Products(Resource):
    def get(self):
        con = sqlite3.connect('storage.db')
        cursor = con.cursor()

        data = path_params.parse_args()
        valid_data = {param:data[param] for param in data if data[param] is not None}
        queryParams = normalize_path_params(**valid_data)

        if not queryParams.get('category'):
            newQuery = "SELECT * FROM products WHERE (price >= ? and price <= ?) LIMIT ? OFFSET ?"
            resultTuple = tuple([queryParams[param] for param in queryParams])
            result = cursor.execute(newQuery, resultTuple)
        else:
            newQuery = "SELECT * FROM products WHERE (price >= ? and price <= ?) and category = ? LIMIT ? OFFSET ?"
            resultTuple = tuple([queryParams[param] for param in queryParams])
            result = cursor.execute(newQuery, resultTuple)

        products = []
        for line in result:
            products.append({
                'productName': line[1],
                'category': line[2],
                'amount': line[3],
                'description': line[4],
                'price': line[5]
            })

        return {'products': products}

class Product(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument('productName', type=str, required=True, help="The field 'productName' cannot be empty.")
    arguments.add_argument('category', type=str)
    arguments.add_argument('amount', type=int, required=True, help="The field 'amount' cannot be empty.")
    arguments.add_argument('description', type=str)
    arguments.add_argument('price', type=float, required=True, help="The product 'price' cannot be empty.")

    def get(self, productId):
        product = ProductModel.find_product(productId)
        if product:
            return product.json()
        return {'message': 'Product not found.'}, 404
    
    @jwt_required
    def post(self, productId):
        if ProductModel.find_product(productId):
            return {"message": "Product id '{}' already exists.".format(productId)}, 400

        data = Product.arguments.parse_args()
        productObject = ProductModel(productId, **data)
        try:
            productObject.save_product()
        except:
            return {'message': 'An internal error occurred while trying to save the data.'}, 500
        return productObject.json()

    @jwt_required
    def put(self, productId):
        data = Product.arguments.parse_args()
        productFound = ProductModel.find_product(productId)

        if productFound:
            productFound.update_product(**data)
            try:
                productFound.save_product()
            except:
                return {'message': 'An internal error occurred while trying to update the data.'}, 500
            return productFound.json(), 200
        return {'messsage': 'Product not found.'}, 404

    @jwt_required
    def delete(self, productId):
        product = ProductModel.find_product(productId)
        if product:
            try:
                product.delete_product()
            except:
                return {'message': 'An internal error occurred while trying to delete the data.'}, 500
            return {'message': 'Product deleted.'}, 200
        return {'message': 'Product not found.'}, 404
from flask_restful import Resource, reqparse
from models.product import ProductModel

class Products(Resource):
    def get(self):
        return {'products': [product.json() for product in ProductModel.query.all()]}

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

    def delete(self, productId):
        product = ProductModel.find_product(productId)
        if product:
            try:
                product.delete_product()
            except:
                return {'message': 'An internal error occurred while trying to delete the data.'}, 500
            return {'message': 'Product deleted.'}, 200
        return {'message': 'Product not found.'}, 404
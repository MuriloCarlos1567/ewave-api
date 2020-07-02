from flask_restful import Resource, reqparse
from models.product import ProductModel

products = [
        {
        'productId': 'porto',
        'productName': 'Vinho do Porto 750ml',
        'category': 'Vinho',
        'amount': 16,
        'description': '',
        'price': 120.00,
        'discount': 10
        },
        {
        'productId': 'tanqueray',
        'productName': 'Gin Tanqueray Dry 750ml',
        'category': 'Gin',
        'amount': 28,
        'description': '',
        'price': 99.99,
        'discount': 0
        },
        {
        'productId': 'dom perignon',
        'productName': 'Champagne Dom Pérignon 750ml',
        'category': 'Champagne',
        'amount': 22,
        'description': '',
        'price': 1189.99,
        'discount': 10
        }
]

class Products(Resource):
    def get(self):
        return {'products': products}

class Product(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument('productName')
    arguments.add_argument('category')
    arguments.add_argument('amount')
    arguments.add_argument('description')
    arguments.add_argument('price')
    arguments.add_argument('discount')

    def find_product(productId):
        for product in products:
            if product['productId'] == productId:
                return product
        return None

    def get(self, productId):
        product = Product.find_product(productId)
        if product:
            return product
        return {'message': 'Product not found.'}, 404
    
    def post(self, productId):
        data = Product.arguments.parse_args()
        productObject = ProductModel(productId, **data)
        newProduct = productObject.json()

        products.append(newProduct)
        return newProduct, 200

    def put(self, productId):
        data = Product.arguments.parse_args()
        productObject = ProductModel(productId, **data)
        newProduct = productObject.json()
        product = Product.find_product(productId)
        if product:
            product.update(newProduct)
            return product, 200
        return {'messsage': 'Product not found.'}, 404

    def delete(self, productId):
        global products
        products = [product for product in products if product['productId'] != productId]
        return {'message': 'Product deleted.'}, 200
from flask_restful import Resource, reqparse
from models.price import PriceModel
from models.product import ProductModel

class PriceCheck(Resource):
    def post(self):
        priceArguments = reqparse.RequestParser()
        priceArguments.add_argument('priceProduct', type=str, required=True)#help
        priceArguments.add_argument('priceAmount', type=int, required=True)#help
        data = priceArguments.parse_args()

        if ProductModel.find_product(data['priceProduct']):
            priceQuery = ProductModel.find_product(data['priceProduct']).json()
            if data['priceAmount'] <= priceQuery['amount']:
                finalPrice = data['priceAmount'] * priceQuery['price']
                return {
                    'priceProduct': data['priceProduct'],
                    'priceAmount': data['priceAmount'],
                    'finalPrice': "%.2f" % finalPrice
                }
            return {"message": "Amount unavaliable. Only '{}' left in stock.".format(priceQuery['amount'])}
        return {'message': 'Product not found.'}, 404
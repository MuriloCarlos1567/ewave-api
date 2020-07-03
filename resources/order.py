from flask_restful import Resource, reqparse
from models.order import OrderModel
from models.user import UserModel
from models.product import ProductModel
from resources.product import Product

class Orders(Resource):
    def get(self):
        return {'orders': [order.json() for order in OrderModel.query.all()]}

class Order(Resource):
    def get(self, orderId):
        order = OrderModel.find_order(orderId)
        if order:
            return order.json()
        return {'message': 'Order not found.'}, 404
    
    def delete(self, orderId):
        order = OrderModel.find_order(orderId)
        if order:
            order.delete_order()
            return {'message': 'Order deleted.'}, 200
        return {'message': 'Order not found.'}, 404

class NewOrder(Resource):
    def post(self):
        arguments = reqparse.RequestParser()
        arguments.add_argument('orderProduct', type=str, required=True)
        arguments.add_argument('orderAmount', type=int, required=True)
        arguments.add_argument('orderPrice', type=float)
        arguments.add_argument('orderEmail', type=str, required=True)
        arguments.add_argument('orderPassword', type=str, required=True)
        data = arguments.parse_args()

        if UserModel.find_by_email(data['orderEmail']):
            passwordCheck = data['orderPassword']
            if passwordCheck == UserModel.check_password(data['orderEmail']):
                productQuery = ProductModel.find_product(data['orderProduct']).json()
                if data['orderAmount'] <= productQuery['amount']:
                    order = OrderModel(**data)
                    order.orderPrice = data['orderAmount'] * productQuery['price']
                    order.save_order()
                    newAmount = productQuery['amount'] - data['orderAmount']
                    return productQuery
                return {'message': 'Sorry. The item is now out of stock.'}
            return {'message': 'Wrong password. Try again.'}
        return {'message': 'User not found.'}


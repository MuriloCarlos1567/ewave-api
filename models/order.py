from sql_alchemy import db

class OrderModel(db.Model):
    __tablename__ = 'orders'

    orderId = db.Column(db.Integer, primary_key=True)
    orderProduct = db.Column(db.String, nullable=False)
    orderAmount = db.Column(db.Integer, nullable=False)
    orderPrice = db.Column(db.Float(precision=2), default=0.0, nullable=False)
    orderEmail = db.Column(db.String, nullable=False)

    def __init__(self, orderProduct, orderAmount, orderPrice, orderEmail, orderPassword):
        self.orderProduct = orderProduct
        self.orderAmount = orderAmount
        self.orderPrice = orderPrice
        self.orderEmail = orderEmail
    
    def json(self):
        return {
            'orderId': self.orderId,
            'orderProduct': self.orderProduct,
            'orderAmount': self.orderAmount,
            'orderPrice': self.orderPrice,
            'orderEmail': self.orderEmail
        }

    def newJson(self):
        return {
            'productId': self.productId,
            'productName': self.productName,
            'category': self.category,
            'amount': self.amount,
            'description': self.description,
            'price': self.price
        }

    @classmethod
    def find_order(cls, orderId):
        order = cls.query.filter_by(orderId=orderId).first()
        if order:
            return order
        return None
        
    def save_order(self):
        db.session.add(self)
        db.session.commit()

    def delete_order(self):
        db.session.delete(self)
        db.session.commit()
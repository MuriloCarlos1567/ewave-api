from sql_alchemy import db

class ProductModel(db.Model):
    __tablename__ = 'products'

    productId = db.Column(db.String(50), primary_key=True)
    productName = db.Column(db.String)
    category = db.Column(db.String(50))
    amount = db.Column(db.Integer)
    description = db.Column(db.String)
    price = db.Column(db.Float(precision=2))

    def __init__(self, productId, productName, category, amount, description, price):
        self.productId = productId
        self.productName = productName
        self.category = category
        self.amount = amount
        self.description = description
        self.price = price
    
    def json(self):
        return {
            'productId': self.productId,
            'productName': self.productName,
            'category': self.category,
            'amount': self.amount,
            'description': self.description,
            'price': self.price
        }
    
    @classmethod
    def find_product(cls, productId):
        product = cls.query.filter_by(productId=productId).first()
        if product:
            return product
        return None
    
    def save_product(self):
        db.session.add(self)
        db.session.commit()

    def update_product(self, productName, category, amount, description, price):
        self.productName = productName
        self.category = category
        self.amount = amount
        self.description = description
        self.price = price

    def delete_product(self):
        db.session.delete(self)
        db.session.commit()
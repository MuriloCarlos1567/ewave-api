class ProductModel:
    def __init__(self, productId, productName, category, amount, description, price, discount):
        self.productId = productId
        self.productName = productName
        self.category = category
        self.amount = amount
        self.description = description
        self.price = price
        self.discount = discount
    
    def json(self):
        return {
            'productId': self.productId,
            'productName': self.productName,
            'category': self.category,
            'amount': self.amount,
            'description': self.description,
            'price': self.price,
            'discount': self.discount
        }
class PriceModel:
    def __init__(self, priceProduct, priceAmount):
        self.priceProduct = priceProduct
        self.priceAmount = priceAmount
    
    def json(self):
        return {
            'priceProduct': self.priceProduct,
            'priceAmount': self.priceAmount
        }



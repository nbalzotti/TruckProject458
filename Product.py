class Product:
    def __init__(self, product_id, weight, volume):
        self.product_id = product_id
        self.weight = weight # in pounds
        self.volume = volume # in cubic meters

    def __str__(self):
        return f"Product ID: {self.product_id}, Weight: {self.weight}, Volume: {self.volume}"
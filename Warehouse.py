class Warehouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.products = []
        self.trucks = []

    def store_product(self, product):
        # Don't know what product will be yet but it will probably store an id, some stats, and a quantity
        self.products.append(product)

    def retrieve_product(self, product):
        if product not in self.products:
            # Not sure what we will do in this case yet, ill just raise an exception for now
            raise Exception("The product is not in the warehouse.")

        # Retrieve the product
        self.products.remove(product)
        return product

    def add_truck(self, truck):
        self.trucks.append(truck)

    def remove_truck(self, truck):
        if truck not in self.trucks:
            # same thing as product
            raise Exception("The truck is not at the warehouse.")

        # Remove the truck
        self.trucks.remove(truck)
        return truck
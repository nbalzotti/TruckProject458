class Truck:
    def __init__(self, x, y, volume_capacity, weight_capacity):
        self.x = x
        self.y = y
        self.volume_capacity = volume_capacity
        self.weight_capacity = weight_capacity
        self.current_volume = 0
        self.current_weight = 0
        self.current_products = []

    def load_product(self, product):
        pass

    def unload_product(self, product):
        pass
    def calculate_fuel_cost(self, distance, fuel_rate):
        pass

    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
class Store:
    def __init__(self, x, y, initial_demand=0):
        self.x = x
        self.y = y
        self.demand = initial_demand

    def generate_demand(self):
        # For now, just increase demand by 1 each time this method is called
        self.demand += 1

    def receive_delivery(self, quantity):
        # Reduce the demand by the quantity delivered
        self.demand = max(0, self.demand - quantity)

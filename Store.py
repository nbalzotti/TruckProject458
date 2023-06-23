class Store:
    def __init__(self, store_id, x, y, initial_demand=5):
        self.id = store_id
        self.x = x
        self.y = y
        self.demand = initial_demand
        self.demand2 = initial_demand
        self.demand3 = initial_demand
        self.node = None
        self.demand_currently_being_fulfilled = False
        
    def assign_node(self, node):
        self.node = node

    def generate_demand(self):
        # For now, just increase demand by 1 each time this method is called
        self.demand += 1
        self.demand2 += 1
        self.demand3 += 1

    def receive_delivery(self, quantity):
        # Reduce the demand by the quantity delivered
        self.demand = max(0, self.demand - quantity)
        self.demand_currently_being_fulfilled = False
        

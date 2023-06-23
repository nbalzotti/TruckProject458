
from Store import Store
from Warehouse import Warehouse
from Road import Road
from Node import Node
from Node import nodeDistance
from Pathfinding import aStar
import matplotlib.pyplot as plt
import numpy as np
from Product import Product

class Truck:
    def __init__(self, truck_id, x, y, weight_capacity, volume_capacity, home_warehouse, max_allowed_speed=50):
        self.id = truck_id
        self.x = x
        self.y = y
        self.current_node = None
        self.volume_capacity = volume_capacity
        self.weight_capacity = weight_capacity
        self.current_volume = 0
        self.current_weight = 0
        self.current_products = {} #dictionary storing lists of product orders by each store name
        self.total_fuel_used = 0
        self.total_distance_traveled = 0
        self.total_time_spent_moving = 0
        self.total_amount_of_product_delivered = 0
        self.max_allowed_speed = max_allowed_speed
        self.path = []
        self.returning = False
        self.stores_to_deliver_to = []
        self.home_warehouse = home_warehouse
        
        #Below are variables for keeping track of how long the truck is going to be doing something.
        
        self.road = None # stores which road the truck is currently traveling on, is none if the truck is not on a road.
        self.road_travel_time_remaining = 0 # In whatever metric the timestep is in
        
        self.store = None # stores which stpre the truck is currently on, is none if the truck is not on a store.
        self.store_offloading_time_remaining = 0 # In whatever metric the timestep is in
        
        self.standby_at_warehouse = None # stores the warehouse the truck is at if the truck is on standby, none if the truck is not at the warehouse or is getting ready to leave (is loading)
        
        self.loading_at_warehouse = None
        self.warehouse_loading_time_remaining = 0 # In whatever metric the timestep is in
    
    
    def calculate_fuel_based_on_speed(self, x):
        # Define the x and y coordinates of the points
        x_values = np.array([2.24, 4.47, 6.70, 11.17, 15.6464, 20.11, 24.58, 26.82, 29.05, 33.528]) # meters per sec
        y_values = np.array([850.29, 1725.43, 1955.66, 2107.5, 2380.8, 2465.83, 2550.86, 2550.86, 2107.5, 2040.69]) # meters per liter
        # performs linear interpolation
        for i in range(len(x_values) - 1):
            if x_values[i] <= x <= x_values[i + 1]:
                slope = (y_values[i + 1] - y_values[i]) / (x_values[i + 1] - x_values[i])
                return y_values[i] + slope * (x - x_values[i])
        return None
            
    def calculate_fuel_usage(self, distance, speed):
        total_extra_weight = 0
        for store_id in self.current_products:
            for product in self.current_products[store_id]:
                total_extra_weight += product[0].weight * product[1]
        return distance / (self.calculate_fuel_based_on_speed(speed) * (1-0.005*(total_extra_weight / 1000)))   #in liters
    
    def calculate_travel_speed(self):
        if self.road is not None:
            return min(self.road.speed_limit, self.max_allowed_speed)
        return min(13.4, self.max_allowed_speed)
    
    def load_product(self, products):
        self.current_products.update(products)
        for store_id in products:
            for product in products[store_id]:
                self.current_volume += product[0].volume 
                self.current_weight += product[0].weight

    def unload_product(self, store_id):
        for product in self.current_products[store_id]:
            self.current_volume -= product[0].volume 
            self.current_weight -= product[0].weight
            self.total_amount_of_product_delivered += product[1]
        return self.current_products.pop(store_id)
    
    def calculate_warehouse_loading_time(self, products):
        # will be some equation based off of weight and number of products, but for now we will return 70 seconds
        loading_time = 0 # in seconds
        for store_id in products:
            for product in products[store_id]:
                loading_time +=  (1 + 0.2 * product[0].volume + 0.01 * product[0].weight) * product[1]  # product[0] = product object, product[1] = quantity
        return loading_time
    
    def calculate_store_offloading_time(self, products, store_id):
        offloading_time = 0 # in seconds
        for product in products[store_id]:
                offloading_time +=  (2 + 0.3 * product[0].volume + 0.02 * product[0].weight) * product[1]  # product[0] = product object, product[1] = quantity
        return offloading_time
    
    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        
    def next_task(self):
        # If the truck is returning, it's moving towards the warehouse
        if self.returning:
            
            # If the next node is the warehouse
            if self.current_node.warehouse is not None:
                # Sets the truck to standby at the warehouse
                self.standby_at_warehouse = self.current_node.warehouse
                
            # If the next node is not a warehouse
            else:
                next_node = self.path[0]
                for road in self.current_node.edges:
                    if road.get_other_node(self.current_node).id == next_node.id:
                        self.road = road
                # Set the travel time
                self.road_travel_time_remaining = self.road.length / self.calculate_travel_speed()
        else:
            # The truck is moving towards a store
            
            # If the next node is a store
            if self.current_node.store is not None and self.current_node.store == self.stores_to_deliver_to[0]:
                self.store = self.current_node.store
                # Set the store offloading time (you might need a method or a constant to get this value)
                self.store_offloading_time_remaining = self.calculate_store_offloading_time(self.current_products, self.store.id) # this just unloads the entire trucks storage, which will only work if we hae 1 store to deliver to. We need to add some more functionality here later
                for product in self.current_products[self.store.id]:
                    self.store.receive_delivery(product[1])
                    
                self.unload_product(self.store.id)
            # If the next node is not a store, it must be a road
            else:
                next_node = self.path[0]
                for road in self.current_node.edges:
                    if road.get_other_node(self.current_node).id == next_node.id:
                        self.road = road
                # Set the travel time
                self.road_travel_time_remaining = self.road.length / self.calculate_travel_speed()
    
    def pass_time(self, sub_time):
        leftover_time = 0
        # If the truck is loading at the warehouse
        if self.loading_at_warehouse is not None:
            print(self.id + " loading up truck at warehouse")
            self.warehouse_loading_time_remaining -= sub_time
            if self.warehouse_loading_time_remaining <= 0: #if it finished task
                leftover_time = abs(self.warehouse_loading_time_remaining)
                if(len(self.stores_to_deliver_to) != 0):
                    self.path = aStar(self.home_warehouse.node, self.stores_to_deliver_to[0].node)
                else:
                    raise Exception("Truck has no stores to deliver to.")
                self.loading_at_warehouse = None
                self.warehouse_loading_time_remaining = 0
                self.returning = False
                self.current_node = self.path.pop(0)
                self.next_task()
        
        # If the truck is offloading at a store
        elif self.store is not None:
            print(self.id +  " offloading product at a store")
            self.store_offloading_time_remaining -= sub_time
            if self.store_offloading_time_remaining <= 0: #if it finished task
                leftover_time = abs(self.store_offloading_time_remaining)
                self.stores_to_deliver_to.pop(0)
                if(len(self.stores_to_deliver_to) == 0): #if truck has no more stores to deliver to, it returns home
                    self.path = aStar(self.store.node, self.home_warehouse.node)
                    self.returning = True
                else:
                    self.path = aStar(self.current_node, self.stores_to_deliver_to[0].node)
                    self.returning = False
                    
                self.store = None
                self.current_node = self.path.pop(0)
                self.next_task()
        
        # If the truck is traveling on a road
        elif self.road is not None:
            self.road_travel_time_remaining -= sub_time
            if self.road_travel_time_remaining <= 0: #if it finished task
                leftover_time = abs(self.road_travel_time_remaining)
                self.total_time_spent_moving += sub_time - leftover_time
                
                # stat stuff
                self.total_distance_traveled += self.road.length
                self.total_fuel_used += self.calculate_fuel_usage(self.road.length, self.calculate_travel_speed())
                
                self.road = None
                self.road_travel_time_remaining = 0
                self.current_node = self.path.pop(0)
                self.update_position(self.current_node.x, self.current_node.y)
                self.next_task()
            else:
                self.total_time_spent_moving += sub_time
        
        # The truck is at standby at the warehouse
        elif self.standby_at_warehouse is not None:
            print(self.id + " standing by at warehouse")
            # Nothing needs to be done, the truck is waiting for a new task
            pass
        
        return leftover_time
    
    
    def calculate_metrics(self):
        metrics = {
            "total_distance_traveled (in meters)": self.total_distance_traveled,
            "total_time_spent_moving (in seconds)": self.total_time_spent_moving,
            "total_amount_of_product_delivered (per unit of product)": self.total_amount_of_product_delivered,
            "total_fuel_used (liter)": self.total_fuel_used,
            "mileage (meters per liter)": self.total_distance_traveled / self.total_fuel_used,
            "total fuel cost acrued (dollars)": self.total_fuel_used * 1.03,
            "average speed (meters per second)": self.total_distance_traveled / self.total_time_spent_moving,
        }
        return metrics
        
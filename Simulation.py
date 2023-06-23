from MapManager import MapManager
import threading
from Pathfinding import aStar
from PIL import Image, ImageTk
import tkinter as tk
from Pathfinding import aStar
from Product import Product
from Node import nodeDistance
class Simulation:
    def __init__(self, lat, lon, dist, Y, time_tick_amount=60, simulation_length=10000, truck_amount = 1, max_simultaneous_delivery_count=1, max_simultaneous_delivery_distance=500):
        self.lat = lat
        self.lon = lon
        self.dist = dist
        self.Y = Y
        self.map_manager = None
        self.active = False
        self.time_tick = 0
        self.time_passed = 0
        self.simulation_length = simulation_length
        self.time_tick_amount = time_tick_amount
        self.truck_amount = truck_amount
        self.max_simultaneous_delivery_count = max_simultaneous_delivery_count
        self.max_simultaneous_delivery_distance = max_simultaneous_delivery_distance

    def start(self):
        self.active = True
        self.map_manager = MapManager(self.lat, self.lon, self.dist, self.Y)
        self.map_manager.generate_map(self.truck_amount)
        #self.simulation_thread = threading.Thread(target=self.run_simulation)
        #self.simulation_thread.start()

    def run_simulation(self):
        window = tk.Tk()
        canvas = tk.Canvas(window, width=1000, height=1000)
        canvas.pack()
        
        self.map_manager.display_map()
        img_path = 'map.png'  # path to your image file
        self.update_image(canvas, img_path)
        
        while self.active:
            print(f"Seconds passed: {self.time_passed}")
            for truck in self.map_manager.trucks:
                time_to_pass = self.time_tick_amount
                while time_to_pass > 0:
                    time_to_pass = truck.pass_time(time_to_pass)
                    
            # I understand this is an absolute mess of loops, my bad
            for truck in self.map_manager.trucks:
                if(truck.standby_at_warehouse is not None):
                    for store in self.map_manager.stores:
                        if store.demand_currently_being_fulfilled == False and store.demand > 5:
                            #print("warehouse", self.map_manager.warehouse.node.x, self.map_manager.warehouse.node.y)
                            #print("store", store.node.x, store.node.y)
                            #self.map_manager.display_map(showplot=True)
                            print(truck.id + " taking delivery order")
                            truck.path = aStar(self.map_manager.warehouse.node, store.node)
                            truck.loading_at_warehouse = truck.home_warehouse
                            truck.standby_at_warehouse = None
                            #print(truck.loading_at_warehouse)
                            truck.returning = False
                            truck.stores_to_deliver_to.append(store)
                            store.demand_currently_being_fulfilled = True
                            
                            product = Product("beef", 500, 3)
                            i = 1
                            while(i < store.demand and truck.current_weight + product.weight * i < truck.weight_capacity and truck.current_volume + product.volume * i < truck.volume_capacity):
                                i += 1
                            product_package = {}
                            product_package[store.id] = []
                            product_package[store.id].append((product, i))
                            truck.load_product(product_package)
                            
                            
                            simultaneous_delivery_count = 1
                            while(truck.current_weight < truck.weight_capacity * 0.8 and truck.current_volume < truck.volume_capacity * 0.8 and simultaneous_delivery_count < self.max_simultaneous_delivery_count): # as long as under 80% capacity and within simultanious delivery bounds
                                for secondary_store in self.map_manager.stores:
                                    if secondary_store.demand_currently_being_fulfilled == False and secondary_store.demand > 5 and nodeDistance(secondary_store.node, store.node) <= self.max_simultaneous_delivery_distance:
                                        truck.stores_to_deliver_to.append(secondary_store)
                                        secondary_store.demand_currently_being_fulfilled = True
                                        
                                        product = Product("beef", 500, 3)
                                        i = 1
                                        while(i < secondary_store.demand and truck.current_weight + product.weight * i < truck.weight_capacity and truck.current_volume + product.volume * i < truck.volume_capacity):
                                            i += 1
                                        product_package = {}
                                        product_package[secondary_store.id] = []
                                        product_package[secondary_store.id].append((product, i))
                                        truck.load_product(product_package)
                                        simultaneous_delivery_count += 1
                                        break
                                break
                            truck.warehouse_loading_time_remaining = truck.calculate_warehouse_loading_time(truck.current_products)
                            time_to_pass = self.time_tick_amount
                            while time_to_pass > 0:
                                time_to_pass = truck.pass_time(time_to_pass)
                            break
                            
            if(self.time_passed % (self.time_tick_amount*100) == 0):   #every 100 ticks           
                self.generate_store_demand()
            
            self.map_manager.display_map()  # This should save the map to 'map.png'
            self.update_image(canvas, img_path)  # Update the displayed image
            self.time_tick += 1
            self.time_passed += self.time_tick_amount
            
            if(self.time_passed > self.simulation_length):
                self.stop()
                self.calculate_all_truck_metrics()
            
        
        

    def generate_store_demand(self):
        for store in self.map_manager.stores:
            store.generate_demand()
    
    def stop(self):
        self.active = False
        #self.simulation_thread.join()

    def update_image(self, canvas, img_path):
        image = Image.open(img_path)
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        canvas.photo = photo
        
    def get_map_image_path(self):
        return 'map.png'  # The MapManager class is saving the map image to 'map.png'
    
    def calculate_all_truck_metrics(self):
        total_metrics = {
            "total_distance_traveled (in meters)": 0,
            "total_time_spent_moving (in seconds)": 0,
            "total_amount_of_product_delivered (per unit of product)": 0,
            "total_fuel_used (liter)": 0,
            "mileage (meters per liter)": 0,
            "total fuel cost acrued (dollars)": 0,
            "average speed (meters per second)": 0,
        }

        for truck in self.map_manager.trucks:
            metrics = truck.calculate_metrics()
            for metric, value in metrics.items():
                total_metrics[metric] += value

        average_metrics = {metric: value / len(self.map_manager.trucks) for metric, value in total_metrics.items()}

        print("Average metrics across all trucks:")
        for metric, value in average_metrics.items():
            print(f"{metric}: {value}")
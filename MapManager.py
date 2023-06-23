import osmnx as ox
import overpy
import random
from Node import Node
from Road import Road
from Store import Store
from Truck import Truck
from Warehouse import Warehouse
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt

class MapManager:
    def __init__(self, lat, lon, dist, Y):
        self.lat = lat
        self.lon = lon
        self.dist = dist
        self.Y = Y
        self.warehouse = None
        self.stores = []
        self.nodes = []
        self.roads = []
        self.trucks = []
        self.graph = None

    def fetch_map(self):
        north, south, east, west = ox.utils_geo.bbox_from_point((self.lat, self.lon), dist=self.dist)
        self.graph = ox.graph_from_bbox(north, south, east, west, network_type='drive')
        
        api = overpy.Overpass()
        query = """
        [out:json];
        (
          node["shop"="supermarket"]({south},{west},{north},{east});
          way["shop"="supermarket"]({south},{west},{north},{east});
          relation["shop"="supermarket"]({south},{west},{north},{east});
        );
        out center;
        """.format(north=north, south=south, east=east, west=west)
        result = api.query(query)
        real_store_locations = [(float(way.center_lon), float(way.center_lat)) for way in result.ways]
        random_stores = random.sample(real_store_locations, min(self.Y, len(real_store_locations)))
        i = 1
        for store in random_stores:
            self.stores.append(Store("Store" + str(i), x=store[0], y=store[1]))
            i += 1

    def create_nodes(self):
        for node in self.graph:
            x, y = self.graph.nodes[node]['x'], self.graph.nodes[node]['y']
            node = Node(node, x, y)
            self.nodes.append(node)

    def get_nearest_node(self, x, y):
        min_distance = float('inf')
        nearest_node = None
        for node in self.nodes:
            distance = ((node.x - x) ** 2 + (node.y - y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest_node = node
        return nearest_node
    
    def assign_stores_to_nodes(self):
        for store in self.stores:
            nearest_node = self.get_nearest_node(store.x, store.y)
            nearest_node.assign_store(store)
            store.assign_node(nearest_node)
            
    def assign_warehouse_to_node(self):
        # Assigning the warehouse to the nearest node to the center of the map
        warehouse_node = self.get_nearest_node(self.lon, self.lat)
        self.warehouse = Warehouse(warehouse_node.x, warehouse_node.y)
        warehouse_node.assign_warehouse(self.warehouse)
        self.warehouse.assign_node(warehouse_node)


    def get_speed_limit(self, speed_limit_str):
        try:
            # Split by space and take the first part, then convert to int
            speed_limit = int(speed_limit_str.split(" ")[0])
            speed_limit = speed_limit * 0.45
        except (ValueError, TypeError, AttributeError):
            # If conversion fails (because of non-numeric string, None, etc.), return 30 mph aka 13.4 meters per second
            speed_limit = 13.4
            
        if speed_limit > 59:
            return 13.4
        return speed_limit

    def create_roads(self):
        for u, v, data in self.graph.edges(keys=False, data=True):
            start_node = next((node for node in self.nodes if node.id == u), None)
            end_node = next((node for node in self.nodes if node.id == v), None)
            length = data['length']
            speed_limit = self.get_speed_limit(data.get('maxspeed'))
            road = Road(u, start_node, end_node, length, speed_limit)
            start_node.edges.append(road)
            end_node.edges.append(road)
            self.roads.append(road)
            
    def create_truck(self):
        # Temporary function to make trucks for the sake of testing display, this should probably be done in warehouse later
        truck = Truck("Truck" + str(len(self.trucks) + 1), self.warehouse.x, self.warehouse.y, 20000, 30, self.warehouse, max_allowed_speed=40)
        truck.current_node = self.warehouse.node
        truck.standby_at_warehouse = self.warehouse
        self.trucks.append(truck)
        
    def generate_map(self, truck_amount):
        self.fetch_map()
        self.create_nodes()
        self.assign_stores_to_nodes()
        self.assign_warehouse_to_node()
        for i in range(truck_amount):
            self.create_truck()
        self.create_roads()
        
        # Temporary traffic for testing
        for road in self.roads:
            road.traffic = random.uniform(0, 1)
        
    def get_map(self):
        return self.graph, self.nodes, self.stores, self.roads
    
    def display_map(self, showplot=False):
        nc = ['g' if node.store is not None else 'b' for node in self.nodes]

        # Assign sizes to nodes
        ns = [50 if node.store is not None else 10 for node in self.nodes]
        
        # Get the traffic values for each road
        traffic_values = [road.traffic for road in self.roads]
        
        # Normalize the traffic values to range [0, 1]
        norm_traffic_values = colors.Normalize(vmin=0, vmax=1)(traffic_values)
        
        # Get a colormap for traffic
        cmap_traffic = cm.get_cmap('Reds')

        # Convert normalized traffic values to RGBA colors
        edge_colors = cmap_traffic(norm_traffic_values)
        
        # Plot the graph
        fig, ax = ox.plot_graph(self.graph, node_color=nc, node_size=ns, node_alpha=0.5, edge_color=edge_colors, edge_linewidth=0.5, show=False, close=False)

        # Adding the warehouse to the plot
        warehouse_marker = plt.scatter(self.warehouse.x, self.warehouse.y, c='g', s=100, marker='8')
        ax.add_artist(warehouse_marker)

        # Adding the trucks to the plot
        for truck in self.trucks:
            truck_marker = plt.scatter(truck.x, truck.y, c='y', s=50, marker='p')
            ax.add_artist(truck_marker)


        if(showplot == True):
            plt.show()
        plt.savefig('map.png')  # Save the map to a file
        plt.close()  # Close the plot to free up memory
        
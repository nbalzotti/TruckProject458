from MapManager import MapManager
import random
import time
from PIL import Image, ImageTk
import tkinter as tk
import threading

def main():
    lat, lon = 47.6097, -122.3331
    dist = 2000  # This is in meters
    Y = 20  # Max number of stores
    
    # Initialize map manager
    map_manager = MapManager(lat, lon, dist, Y)
    map_manager.generate_map()

    # Create a tkinter window
    window = tk.Tk()

    # Create a canvas to hold the image
    canvas = tk.Canvas(window, width=1000, height=1000)
    canvas.pack()
    
    map_manager.display_map()
    img_path = 'map.png'  # path to your image file
    update_image(canvas, img_path)

    # Moving trucks to random nodes for testing purposes
    for i in range(10):  # simulate 10 time ticks
        print(f"Time tick: {i}")
        for truck in map_manager.trucks:
            random_node = random.choice(map_manager.nodes)
            truck.update_position(random_node.x, random_node.y)
        map_manager.display_map()  # This should save the map to 'map.png'
        update_image(canvas, img_path)  # Update the displayed image

    window.mainloop()  # Start the GUI event loop

def update_image(canvas, img_path):
    image = Image.open(img_path)
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    canvas.photo = photo


if __name__ == "__main__":
    main()
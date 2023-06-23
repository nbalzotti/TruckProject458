from Simulation import Simulation


def main():
    # These parameters need to be defined or generated
    lat, lon = 47.6297, -122.3331   #original coordinates
    #lat, lon = 47.6597, -122.3431
    dist = 2000
    Y = 10

    # Create a new Simulation
    simulation = Simulation(lat, lon, dist, Y, time_tick_amount=30, simulation_length=2000, truck_amount=2,max_simultaneous_delivery_count=2)

    # Start the simulation
    simulation.start()
    # Run the simulation
    simulation.run_simulation()


if __name__ == "__main__":
    main()
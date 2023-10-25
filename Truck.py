class Truck:
    def __init__(self, truck_id, speed=18):
        self.truck_id = truck_id
        self.speed = speed
        self.packages = []
        self.total_distance_travelled = 0
        self.current_address = '4001 South 700 East'
        self.delivery_history = {}

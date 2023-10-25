class Package:
    def __init__(self, id, address, deadline, city, state, zip_code, weight, special_note, status):
        self.id = id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.weight = weight
        self.special_note = special_note
        self.status = status
        self.delivery_time = None

    def __str__(self):
        return f'Package ID: {self.id}, Address: {self.address}, Deadline: {self.deadline}, City: {self.city}, State: {self.state}, ZIP: {self.zip_code}, Weight: {self.weight}, Special Note: {self.special_note}, Status: {self.status}, Delivered at: {self.delivery_time}'

import csv
from datetime import datetime

from Hash_Table import HashTable
from Package import Package
from Truck import Truck


# Function to load the package data into the hash_table
def loadPackageData(hash_table):
    with open('mydata/packages.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # CSV columns:
            id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            deadline = row[5]
            weight = row[6]
            special_note = row[7]
            status = "At the hub"  # Initial status for all packages
            # Create Package object and insert into HashTable
            package = Package(id, address, deadline, city, state, zip_code, weight, special_note, status)
            hash_table.insert(id, package)


# Create a hash table
hash_table = HashTable()

# Load packages from CSV into hash table
loadPackageData(hash_table)


def loadDistanceData():
    distanceData = []
    with open('mydata/distances.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # Convert each distance to a float, and append the result to distanceData
            distanceRow = [float(distance) if distance else None for distance in row]
            distanceData.append(distanceRow)
    return distanceData


distanceData = loadDistanceData()


# Define loadAddressData function
def loadAddressData():
    addressData = []
    with open('mydata/address_list.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # Read in the second and third column
            place_name = row[1]
            address = row[2]
            addressData.append((place_name, address))
    return addressData


# Load the address data
addressData = loadAddressData()


def distanceBetween(address1, address2):
    # Find the indexes of the two addresses
    index1 = next(i for i, v in enumerate(addressData) if v[1] == address1)
    index2 = next(i for i, v in enumerate(addressData) if v[1] == address2)
    # If the distances are not found in the two-dimensional, give the inverse
    if distanceData[index1][index2] is None:
        return distanceData[index2][index1]
    # Return the corresponding distance
    return distanceData[index1][index2]


def minDistanceFrom(fromAddress, truckPackages):
    # Initialize minimum distance and corresponding address
    min_distance = float('inf')
    min_address = None

    # Iterate through all the packages in the truck
    for package in truckPackages:
        # Get the delivery address for the current package
        current_address = package['Delivery Address']
        # Get the distance from the fromAddress to the current address
        current_distance = distanceBetween(fromAddress, current_address)

        # Update minimum distance and corresponding address if current distance is smaller
        if current_distance < min_distance:
            min_distance = current_distance
            min_address = current_address

    # Return the address with minimum distance
    return min_address


# Truck 1 is the early truck that will handle early/grouped packages and take over Truck 3 once done
# Truck 2 is the late truck that gets the deliveries for 9:05 AM delay and packages required to be on Truck 2
# Truck 3 is the wrap-up truck for everything else/mostly EOD packages and wrong listed address #9
def truckLoadPackages(trucks):
    truck1_packages = [1, 13, 14, 15, 16, 19, 20, 21, 29, 30, 34, 37]
    truck2_packages = [3, 6, 18, 25, 26, 28, 31, 32, 36, 38, 39, 40]
    truck3_packages = [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 22, 23, 24, 27, 33, 35]

    for i in range(1, 41):
        package = hash_table.lookup(i)

        if package.id in truck1_packages:
            trucks[0].packages.append(package)
        elif package.id in truck2_packages:
            trucks[1].packages.append(package)
        elif package.id in truck3_packages:
            trucks[2].packages.append(package)


# Initialization
truck1 = Truck(1)
truck2 = Truck(2)
truck3 = Truck(3)
trucks = [truck1, truck2, truck3]

# Call the function
truckLoadPackages(trucks)

import datetime


def truckDeliverPackages(truck):
    # Start delivering from the hub, so initialize current_address
    current_address = '4001 South 700 East'

    if truck.truck_id == 1:
        # Truck 1 Start time set at 8:00AM for early start
        current_time = datetime.datetime.now().replace(hour=8, minute=00, second=00)
    if truck.truck_id == 2:
        # Truck 2 Start time set at 9:05AM for delivery of late packages
        current_time = datetime.datetime.now().replace(hour=9, minute=5, second=00)
    if truck.truck_id == 3:
        # Truck 3 Start time set right after Truck 1 comes back to hub
        current_time = datetime.datetime.now().replace(hour=10, minute=20, second=40)

    # While there are still packages in the truck
    while truck.packages:
        # Find the closest package's delivery address from the current location
        min_distance_address = min(truck.packages,
                                   key=lambda package: distanceBetween(current_address, package.address)).address

        # Calculate the distance from the current location to the next location
        distance = distanceBetween(current_address, min_distance_address)

        # Calculate the time it takes to deliver
        time_to_deliver = datetime.timedelta(hours=distance / truck.speed)
        current_time += time_to_deliver

        # Update the truck's total distance traveled
        truck.total_distance_travelled += distance

        # Update the current address
        current_address = min_distance_address

        # Deliver the packages at the current address
        for package in truck.packages:
            if package.address == current_address:
                # Add the package to the delivery history with the delivery time
                truck.delivery_history[package.id] = current_time.strftime('%H:%M:%S')

                # Update package delivery status and time in hash table
                hash_table.lookup(package.id).status = 'Delivered'
                hash_table.lookup(package.id).delivery_time = current_time.strftime('%H:%M:%S')

                # Remove the package from the truck
                truck.packages.remove(package)

    # Return back to the hub after all deliveries, updating the total distance traveled
    distance_to_hub = distanceBetween(current_address, '4001 South 700 East')
    time_to_hub = datetime.timedelta(hours=distance_to_hub / truck.speed)
    current_time += time_to_hub
    truck.total_distance_travelled += distance_to_hub


for truck in trucks:
    truckDeliverPackages(truck)

total_milage = 0

for truck in trucks:
    total_milage += truck.total_distance_travelled


# UI for the user to view the delivery status of package(s)
def main_menu():
    while True:
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("1. Print All Package Status and The Total Mileage")
        print("2. Get a Single Package Status with a Time")
        print("3. Get All Package Status with a Time")
        print("4. Exit")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        try:
            selection = int(input("Enter your selection: "))
        except ValueError:
            print("Invalid selection. Please enter a number between 1 and 4.")
            continue

        if selection == 1:
            print_all_package_status_and_total_mileage()
        elif selection == 2:
            package_id = input("Enter package id: ")
            time = input("Enter time (in 24-hour format 'HH:MM:SS'): ")
            get_single_package_status_with_time(package_id, time)
        elif selection == 3:
            time = input("Enter time (in 24-hour format 'HH:MM:SS'): ")
            get_all_package_status_with_time(time)
        elif selection == 4:
            print("Exiting the program.")
            break
        else:
            print("Invalid selection. Please enter a number between 1 and 4.")


# Function to print all the package info and total mileage
def print_all_package_status_and_total_mileage():
    print("Cumulative Mileage of Trucks: ",
          truck1.total_distance_travelled + truck2.total_distance_travelled + truck3.total_distance_travelled, "miles")
    for i in range(1, 41):  # Assuming package IDs are 1 through 40
        package = hash_table.lookup(i)
        print(f"Package ID: {package.id}, Delivery Status: {package.status}, Delivered at: {package.delivery_time}, "
              f"Address: {package.address}, Deadline: {package.deadline}, City: {package.city}, "
              f"Zip Code: {package.zip_code}, Weight: {package.weight}")


# Function to print info of single package
def get_single_package_status_with_time(package_id, time):
    package = hash_table.lookup(int(package_id))
    status_at_time = check_time(package.id, time)
    print(f"Package ID: {package.id}, Status at {time}: {status_at_time}, Delivery Time: {package.delivery_time}, "
              f"Address: {package.address}, Deadline: {package.deadline}, City: {package.city}, "
              f"Zip Code: {package.zip_code}, Weight: {package.weight}")


# Function to print all the package at a specific time
def get_all_package_status_with_time(time):
    for i in range(1, 41):  # Assuming package IDs are 1 through 40
        package = hash_table.lookup(i)
        status_at_time = check_time(package.id, time)
        print(f"Package ID: {package.id}, Status at {time}: {status_at_time}, Delivery Time: {package.delivery_time}, "
              f"Address: {package.address}, Deadline: {package.deadline}, City: {package.city}, "
              f"Zip Code: {package.zip_code}, Weight: {package.weight}")


# Function to convert strings into datetime.datetime objects
def convert_datetime(string):
    (h, m, s) = string.split(":")
    converted_string = datetime.datetime.now().replace(hour=int(h), minute=int(m), second=int(s))
    return converted_string


# Function to check what status the package was at a specific hour
def check_time(package_id, time):
    # Convert the package delivery time to datetime.datetime object
    converted_time = convert_datetime(time)
    # Check if the package is in the truck's delivery history
    if package_id in truck1.delivery_history.keys():
        truck1_start = datetime.datetime.now().replace(hour=8, minute=00, second=00)
        truck1_delivered_at = convert_datetime(truck1.delivery_history[package_id])
        # If package is before the truck leaves it is in the hub
        if converted_time < truck1_start:
            return "At Hub"
        # If the package is between the delivery time and the start of the truck return "en route"
        elif truck1_start < converted_time < truck1_delivered_at:
            return "En Route"
        else:
            return "Delivered"
    # Repeat previous method for other two trucks
    elif package_id in truck2.delivery_history.keys():
        truck2_start = datetime.datetime.now().replace(hour=9, minute=5, second=00)
        truck2_delivered_at = convert_datetime(truck2.delivery_history[package_id])
        if converted_time < truck2_start:
            return "At Hub"
        elif truck2_start < converted_time < truck2_delivered_at:
            return "En Route"
        else:
            return "Delivered"
    else:
        truck3_start = datetime.datetime.now().replace(hour=10, minute=20, second=40)
        truck3_delivered_at = convert_datetime(truck3.delivery_history[package_id])
        if converted_time < truck3_start:
            return "At the Hub"
        elif truck3_start < converted_time < truck3_delivered_at:
            return "En Route"
        else:
            return "Delivered"


# Run the main menu when the script is run
if __name__ == "__main__":
    main_menu()

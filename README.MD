# Optimizing Package Delivery with Python

## Introduction

In this project, I have developed a Python-based solution to efficiently manage and optimize package deliveries. I have created a robust system that handles package data, calculates optimal routes, and provides real-time delivery status updates.

## Problem Statement

The primary challenge in package delivery management is to ensure that packages are delivered to their respective destinations in the most efficient and timely manner. This involves several key tasks:

1. **Loading Package Data:** I start by loading package data from a CSV file, which includes information such as package IDs, delivery addresses, deadlines, weights, and special notes.
2. **Routing and Scheduling:** Once I have the package data, I need to determine the optimal routes for delivery. This involves creating a schedule for multiple trucks, each with its own set of packages. I must consider factors like delivery deadlines and package priorities.
3. **Real-Time Tracking:** To provide transparency and real-time updates to My users, I need to track the status of each package as it moves from the hub to its destination. This includes updating delivery times and statuses.
4. **User Interface:** Lastly, I offer a user-friendly interface for users to query package statuses, check delivery times, and view total mileage.

## Solution Overview

### Data Management

We use a hash table to efficiently store and manage package data. Each package is represented as an object with attributes such as package ID, delivery address, deadline, weight, and status. The hash table allows us to quickly access and update package information.

### Routing and Scheduling

To optimize delivery routes, I divide packages among three trucks: early, late, and wrap-up trucks. Each truck is assigned specific packages based on their priorities and deadlines. I calculate the distances between addresses and use this data to determine the shortest path for each truck.

### Real-Time Tracking

We implement real-time tracking by continuously updating the status and delivery times of packages as they are delivered. This information is stored in the hash table and can be queried by users.

### User Interface

We provide a user-friendly command-line interface that allows users to interact with the system. Users can query the status of a single package at a specific time, view the status of all packages at a given time, and obtain the total mileage traveled by all trucks.

## Key Components

### Hash Table (`HashTable.py`)

The hash table is the core data structure used to store and retrieve package information efficiently. It supports insertion and lookup operations, making it easy to manage package data.

### Package Class (`Package.py`)

The Package class defines the structure of a package object, including attributes such as ID, address, deadline, weight, and status. It also handles the conversion of package delivery times.

### Truck Class (`Truck.py`)

The Truck class represents a delivery truck and includes attributes such as truck ID, speed, packages, total distance traveled, current address, and delivery history. It also contains the logic for package delivery.

### Main Program (`main.py`)

The main program coordinates all the components. It loads package data, calculates distances, assigns packages to trucks, tracks deliveries, and provides a user interface for interaction.

## Conclusion

With this Python-based package delivery management system, I have successfully addressed the challenges of efficient routing, real-time tracking, and user-friendly interaction. This project demonstrates how Python can be used to optimize logistics and improve package delivery operations. My solution not only streamlines the process but also enhances customer satisfaction by providing transparency and timely updates.

By combining my extensive Python programming experience with effective data structures and algorithms, I have created a reliable and scalable solution that can be further expanded and customized to meet the specific needs of package delivery services.

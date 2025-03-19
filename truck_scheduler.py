import math
import pika
from db import cursor
import re
#global variable for the max distance a truck can travel in a day
MAX_DISTANCE = 15

#stores the locations of all the houses
HOUSE_GRID = []

#stores the weekly schedule with each index including
# 1. the truck type involved in the pickup
# 2. the house being picked up from
# Create a dictionary to store the schedule by day and truck type
WEEKLY_SCHEDULE = {
    "Sunday": {"Garbage": [], "Recycling": [], "Organic": []},
    "Monday": {"Garbage": [], "Recycling": [], "Organic": []},
    "Tuesday": {"Garbage": [], "Recycling": [], "Organic": []},
    "Wednesday": {"Garbage": [], "Recycling": [], "Organic": []},
    "Thursday": {"Garbage": [], "Recycling": [], "Organic": []},
    "Friday": {"Garbage": [], "Recycling": [], "Organic": []},
    "Saturday": {"Garbage": [], "Recycling": [], "Organic": []},
}
# set up the connection to RabbitMQ and initizalizes the channels being used
def setup_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='Truck-Queue')
    return connection, channel

# set up listening to the Truck Queue
def run_rabbitmq_listener():
    connection, channel = setup_rabbitmq()
    channel.basic_consume(queue='Truck-Queue', on_message_callback=rabbitmq_callback, auto_ack=True)
    print("[Truck Scheduler] Listening for requested trucks...")
    channel.start_consuming()

# callback function to process trucks from the Truck Queue
def rabbitmq_callback(ch, method, properties, body):
    message = body.decode()
    """Extracts request ID, house ID, and trucks needed from the message string."""

    # Regular expression to capture request ID, house ID, and truck types
    match = re.match(r"Request ID:\s*(\d+),\s*House ID:\s*(\d+),\s*Truck Needed:\s*(.*)", message)

    if not match:
        raise ValueError("Invalid message format")

    request_id = int(match.group(1))  # Extract and convert request ID
    house_id = int(match.group(2))  # Extract and convert house ID
    trucks_needed = [truck.strip() for truck in match.group(3).split(",")]  # Split truck list and remove spaces
    days_scheduled = list()
    for truck in trucks_needed:
        day = schedule_truck_route(house_id, truck)
        if day == 0:
            print("Could not find day to schedule truck, reached max cap for weekly schedule...")
            day = "N/A"
        days_scheduled.append(day)

    publish_truck_info_to_queue(request_id, house_id, trucks_needed,days_scheduled)

# publishes trucks scheduled information to SQL
def publish_truck_info_to_queue(request_id, house_id,truck_type,days_visiting):
    # Insert data into schedule
    cursor.execute("INSERT INTO schedule (request_id, house_id,truck_type,day_visiting) VALUES (?, ?,?,?)",
                   (request_id, house_id, truck_type, days_visiting))


#helper function to calculate the distance between 2 houses
def distance_between_houses (house_id_1,house_id_2):
    if house_id_1 not in HOUSE_GRID or house_id_2 not in HOUSE_GRID:
        raise ValueError("Invalid house ID(s).")

    x1, y1 = HOUSE_GRID[house_id_1]
    x2, y2 = HOUSE_GRID[house_id_2]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


#helper function to calculate the distance a truck is covering with the input houses
def truck_route_distance_if_house_added(houses):
    distance = 0
    distance += distance_between_houses(0, houses[0]) #add distance from base to house 1
    previous_house = houses[0]
    for house in houses:
        distance += distance_between_houses(previous_house, house)
        previous_house = house
    return distance

#schedules a truck to pass by the house, returns the day it will pass by
#makes use of helper function truck_route_distance
def schedule_truck_route(house_id, truck_needed):
    for day, trucks in WEEKLY_SCHEDULE.items():
        for truck, houses in trucks.items():
            if truck == truck_needed:
                temp_houses = houses
                temp_houses.append(house_id)
                print(f"Distance calculated if house were appended to this day:",truck_route_distance_if_house_added(temp_houses))
                if truck_route_distance_if_house_added(temp_houses) < MAX_DISTANCE:
                    return day
    return 0


# reads the coordinates of the houses from the text file coordinates.txt and saves them
# to global variable HOUSE_GRID
def get_all_house_coordinates():
    # Fetch all data from the map table
    cursor.execute("SELECT * FROM map")
    rows = cursor.fetchall()
    map_data = {}
    for house_id, x_value, y_value in rows:
        HOUSE_GRID[house_id] = (x_value, y_value)

#gets the current schedule and stores it in a global data structure
def get_current_schedule():
  # Fetch all data from the map table
    cursor.execute("SELECT * FROM schedule")
    rows = cursor.fetchall()
    # Loop through each row and organize the data
    for row in rows:
        request_id, house_id, truck_types, days = row
        truck_types = truck_types.strip('[]').split(', ')
        days = days.strip('[]').split(', ')

        # Fill the WEEKLY_SCHEDULE dictionary
        for day, truck_type in zip(days, truck_types):
                WEEKLY_SCHEDULE[day][truck_type].append(house_id)


# main function to set up the truck_scheduler
def main():
    # set up RabbitMQ connection and channel
    connection, channel = setup_rabbitmq()

    # set the scheduler to listen on the Truck-Queue and process incoming requests
    print("Waiting for messages in Truck-Queue...")

    # subscribe to the Truck-Queue to get requests
    channel.basic_consume(queue='Truck-Queue',
                          on_message_callback=lambda ch, method, properties, body: rabbitmq_callback(ch, method, properties,body))
    # start listening for messages
    channel.start_consuming()

if __name__ == "__main__":
    main()

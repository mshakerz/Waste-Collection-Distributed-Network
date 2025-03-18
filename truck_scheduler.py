#global variable for the max distance a truck can travel in a day
MAX_DISTANCE = 15

#stores the locations of all the houses
HOUSE_GRID = {}

#stores the weekly schedule with each index including
# 1. the truck type involved in the pickup
# 2. the house being picked up from
WEEKLY_SCHEDULE=[]

# set up the connection to RabbitMQ and initizalizes the channels being used
def setup_rabbitmq():

# set up listening to the Truck Queue
def run_rabbitmq_listener():

# callback function to process trucks from the Truck Queue
def rabbitmq_callback(ch, method, properties, body):

# publishes trucks scheduled information to Scheduled Queue
def publish_truck_info_to_queue():

#helper function to calculate the distance between 2 houses
def distance_between_houses (house_id_1,house_id_2):

#helper function to calculate the distance a truck is covering with the input houses
def truck_route_distance(houses):

#schedules a truck to pass by the house, returns the day it will pass by
#makes use of helper function truck_route_distance
def schedule_truck_route(houses):

# reads the coordinates of the houses from the text file coordinates.txt and saves them
# to global variable HOUSE_GRID
def get_all_house_coordinates():

# main function to set up the truck_scheduler
def main():

if __name__ == "__main__":
    main()

import pika
import sqlite3
import random
import sys
import json

#max size of the neighbourhodd for houses to be collected from
GRID_SIZE = (10, 10)


#setting up mqerver
def setup_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    #setup connection to Garbage Info Queue
    channel.queue_declare(queue='Garbage-Info-Queue', durable=True)

    return connection, channel


#publish house waste info to queue
def publish_house_info_to_queue(house_id):
    connection, channel = setup_rabbitmq()

    garbage_data = {
        "Request ID": random.randint(1000, 9999),  #randon req id is made
        "house_id": house_id,
        "garbage_info": generate_waste_percentages(),
        "location": get_house_coordinates(house_id),
        "day_and_time": "2025-03-20 10:00 AM"  #random timestamp
    }

    channel.basic_publish(exchange='', routing_key='Garbage-Info-Queue', body=json.dumps(garbage_data))
    print(f"Garbage info has been sent → {garbage_data}")

    connection.close()


#randomly generate garbage percentages (values always increasing up to 100)
def generate_waste_percentages():
    waste_types = ["Garbage", "Recycling", "Organic"]
    percentages = []

    for _ in waste_types: #https://pynative.com/python-random-randrange/
        prev_value = random.randint(50, 80)  #higher chance of getting over 80 on first go
        new_value = min(prev_value + random.randint(10, 30), 100)  #inc but don't go over 100
        percentages.append(new_value)

    return percentages

#get house coordinates from the db from map table
def get_house_coordinates(house_id): #https://www.askpython.com/python/examples/python-sql-data-to-json
    #https://docs.python.org/3/library/sqlite3.html
    conn = sqlite3.connect("my_database.db")  #setup/connect to db
    cursor = conn.cursor()

    cursor.execute("SELECT x_value, y_value FROM map WHERE house_id = ?", (house_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return {"x": result[0], "y": result[1]}
    else:
        return {"x": -1, "y": -1}  #invalid location in case we can't find the house


#main to call
def run(house_id):
    publish_house_info_to_queue(house_id)


#runs program
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <house_id>")
        sys.exit(1)

    house_id = int(sys.argv[1])  #make sure house id is taken at terminal
    run(house_id)

import pika
import json

# Threshold for requesting a truck
THRESHOLD = 80

# Function to set up the RabbitMQ connection and declare necessary queues
def setup_rabbitmq():
    """
    Establishes a connection to RabbitMQ and declares the required queues.
    - 'Garbage-Info-Queue': Receives garbage data from clients.
    - 'Truck-Queue': Sends truck requests to the truck scheduler.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='Garbage-Info-Queue', durable=True)  # Ensures messages persist if RabbitMQ restarts
    channel.queue_declare(queue='Truck-Queue', durable=True)
    return connection, channel


# Callback function to process waste data from the Garbage Info Queue
def rabbitmq_callback(ch, method, properties, body):
    """
    Callback function triggered when a message is received from the Garbage-Info-Queue.
    Parses the received message, checks waste levels, and sends a truck request if needed.
    """
    message = json.loads(body.decode())
    house_id = message['house_id']  # ID of the house reporting waste data
    garbage_data = message['garbage_info']  # List containing waste percentages for each type

    trucks_needed = []
    waste_types = ['Garbage', 'Recycling', 'Organic']  # Three types of waste collected

    # Check if waste levels exceed the threshold, and determine required trucks
    for i, waste in enumerate(garbage_data):
        if waste > THRESHOLD:
            trucks_needed.append(waste_types[i])

    # If trucks are needed, send a truck request to the Truck Queue
    if trucks_needed:
        print(f"[Server] Processed house {house_id}: Needed trucks {trucks_needed}")
        publish_truck_info_to_queue(house_id, trucks_needed)

    #print(f"[Server] Processed house {house_id}: Needed trucks {trucks_needed}")


# Function to publish truck request messages to the Truck Queue
def publish_truck_info_to_queue(house_id, trucks_needed):
    """
    Publishes truck request messages to the Truck Queue when waste exceeds the threshold.
    """
    connection, channel = setup_rabbitmq()
    request_id = house_id  # Using house_id as a temporary request ID for simplicity
    message = f"Request ID: {request_id}, House ID: {house_id}, Truck Needed: {', '.join(trucks_needed)}"
    channel.basic_publish(exchange='', routing_key='Truck-Queue', body=message)
    print(f"[Server] Published truck request for House {house_id}: {trucks_needed}\n")
    connection.close()


# Function to start listening for messages from the Garbage Info Queue
def run_rabbitmq_listener():
    """
    Listens for incoming messages from the Garbage Info Queue.
    When a message is received, it is processed by rabbitmq_callback().
    """

    connection, channel = setup_rabbitmq()
    channel.basic_consume(queue='Garbage-Info-Queue', on_message_callback=rabbitmq_callback, auto_ack=True)
    print("[Server] Listening for waste data from clients...")
    try:
        channel.start_consuming()  # Continuously listens for new messages
    except KeyboardInterrupt:
        print("[Server] Stopping RabbitMQ listener...")
        connection.close()


# Main entry point for running the server
if __name__ == "__main__":
    run_rabbitmq_listener()

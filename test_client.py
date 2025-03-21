import pika
import json


# Function to set up RabbitMQ connection
def setup_rabbitmq():
    """
    Establishes a connection to RabbitMQ and declares the required queue.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='Garbage-Info-Queue', durable=True)  # Ensure messages persist if RabbitMQ restarts
    return connection, channel


# Function to send a test message to the Garbage Info Queue
def send_test_message():
    """
    Sends a test waste data message to the Garbage Info Queue to simulate a client request.
    """
    connection, channel = setup_rabbitmq()

    # Define a sample waste report from a house
    test_message = {
        "house_id": 5,
        "garbage_info": [85, 40, 90]  # Garbage: 85%, Recycling: 40%, Organic: 90%
    }

    # Convert the message to JSON format and publish it
    channel.basic_publish(
        exchange='',
        routing_key='Garbage-Info-Queue',
        body=json.dumps(test_message)
    )

    print(f"[Test Client] Sent test message: {test_message}")
    connection.close()


# Run the test client
if __name__ == "__main__":
    send_test_message()

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Purge the queue
channel.queue_purge(queue='Truck-Queue')
channel.queue_purge(queue='Garbage-Info-Queue')

print("Queue purged successfully.")
connection.close()
#threshold for requesting a truck
THRESHOLD = 80

# set up the connection to RabbitMQ and initizalizes the channels being used
def setup_rabbitmq():

# set up listening to the Garbage Info Queue
def run_rabbitmq_listener():

# callback function to process trucks from the Garbage Info Queue
def rabbitmq_callback(ch, method, properties, body):

# publishes trucks needed information to Truck Queue
def publish_truck_info_to_queue():

# set Up listening to the Garbage Info Queue
def run_rabbitmq_listener():


# start gRPC server
def serve():

if __name__ == "__main__":
    serve()

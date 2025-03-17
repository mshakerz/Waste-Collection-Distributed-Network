#threshold for requesting a truck
THRESHOLD = 80

# set up the connection to RabbitMQ and initizalizes the channels being used
def setup_rabbitmq():

# set up listening to the Garbage Info Queue
def run_rabbitmq_listener():

# callback function to process mines from the Garbage Info Queue
def rabbitmq_callback(ch, method, properties, body):

# publishes trucks needed information to Truck Queue
def publish_truck_info_to_queue():

class TruckControlServicer(truck_control_pb2_grpc.TruckControlServicer):
    # implement the trucks needed for each house
    # index 0 -- >Waste
    # index 1 --> Recycling
    # index 2 --> Organic
    def GetTrucksNeeded(self,request, context):

    trucks_needed = []
    for garbage_info in request.garbage_info:
        if garbage_info > THRESHOLD:
            trucks_needed.append(1)
        trucks_needed.append(0)

    return truck_control_pb2.TruckNeededResponse(
        flat_map=trucks_needed
    )

# set Up listening to the Garbage Info Queue
def run_rabbitmq_listener():


# start gRPC server
def serve():

if __name__ == "__main__":
    serve()

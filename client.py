# Constants
COORDINATES = {}

grid_size = (10, 10)

#set up the connection to RabbitMQ and initizalizes the channels being used
def setup_rabbitmq():

# set up listening to the Scheduled Queue
def run_rabbitmq_listener():

# callback function to process mines from the Scheduled Queue
def rabbitmq_callback(ch, method, properties, body):

#publishes garbage information to Garbage Info Queue
def publish_house_info_to_queue():

#randomly generates a percentage with subsequent values increasing but never greater than 100
#for any type of garbage generated
def random_percentage_generator(previous_value):

#reads the coordinates of the current house from the text file coordinates.txt and saves them
#to global variable COORDINATES
def get_house_coordinates(house_id):

def run(house_id):

if __name__ == "__main__":
    house_id= int(sys.argv[1])
    run(house_id)

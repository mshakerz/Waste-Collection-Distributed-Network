# coe892

Assume data message on Truck Queue takes form of 

"Request ID: xxx, House ID: xxx, Truck Needed: a, b , c"

Distance between houses is Euclidean with Max distance travelled by a truck (not including return to home base) equal to 15 units

docker restart rabbitmq (wait for like 15 seconds)
docker ps (to verify docker is running successfully)

python db.py
python server.py
python truck_scheduler.py
python client.py
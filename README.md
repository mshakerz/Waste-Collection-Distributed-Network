Steps to Run:
docker start mqserver
python db.py
python server.py
python truck_scheduler.py
python client.py # (should add an int between 1 - 10 in place of #)
When wanting to re-test/run, clean/clear the database by running: python dbClean.py
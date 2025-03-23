Steps to Run:
docker start mqserver
python db.py
python server.py
python truck_scheduler.py
python client.py # (should add an int between 1 - 10 in place of #)
python WasterCollectionUI.py (run only after there is info in the schedule table)
When wanting to re-test/run, clean/clear the database by running: python dbClean.py
To purge the queues run purge.py
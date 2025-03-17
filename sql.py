import sqlite3

# Connect to a database (or create one if it doesn't exist)
conn = sqlite3.connect("my_database.db")

# Create a cursor object
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS schedule;")
cursor.execute("DROP TABLE IF EXISTS map;")

# Create a table
cursor.execute("""
CREATE TABLE schedule (
    request_id INTEGER PRIMARY KEY,
    house_id INTEGER,
    truck_type TEXT[],
    day_visiting TEXT[]
)
""")

# Create a table
cursor.execute("""
CREATE TABLE map (
    house_id INTEGER PRIMARY KEY,
    x_value INTEGER,
    y_value INTEGER
)
""")


# Insert data into schedule
cursor.execute("INSERT INTO schedule (request_id, house_id,truck_type,day_visiting) VALUES (?, ?,?,?)",
               (1, 101,"Waste", "Monday"))

# Insert data into map
cursor.execute("INSERT INTO map (house_id, x_value, y_value) VALUES (?, ?, ?)",
               (101, 34, 78))

# Commit and close
conn.commit()
conn.close()

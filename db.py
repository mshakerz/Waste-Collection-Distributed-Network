import sqlite3

# Connect to a database (or create one if it doesn't exist)
conn = sqlite3.connect("my_database.db")

# Create a cursor object
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS schedule;")
cursor.execute("DROP TABLE IF EXISTS map;")

# Create a table
# truck_type can be only the following:
#  Garbage, Recycling, Organic
# day can be any day of the week assuming we are only take about 1 week
#possible values are Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday
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
#acceptable values for truck_type is
#Garbage , Recycling and Organic
cursor.execute("INSERT INTO schedule (request_id, house_id,truck_type,day_visiting) VALUES (?, ?,?,?)",
               (1, 101,"Waste", "Monday"))

# Insert data into map
#house id --> 0 means home base of trucks
cursor.execute("INSERT INTO map (house_id, x_value, y_value) VALUES (?, ?, ?)",
               (0, 5, 5),
               )
cursor.execute("INSERT INTO map (house_id, x_value, y_value) VALUES (?, ?, ?)",
               (1, 1, 1),
               )
cursor.execute("INSERT INTO map (house_id, x_value, y_value) VALUES (?, ?, ?)",
               (2, 2, 3),
               )
cursor.execute("INSERT INTO map (house_id, x_value, y_value) VALUES (?, ?, ?)",
               (3, 3, 4),
               )
cursor.execute("INSERT INTO map (house_id, x_value, y_value) VALUES (?, ?, ?)",
               (4, 5, 6),
               )
cursor.execute("INSERT INTO map (house_id, x_value, y_value) VALUES (?, ?, ?)",
               (5, 2, 8),
               )
cursor.execute("INSERT INTO map (house_id, x_value, y_value) VALUES (?, ?, ?)",
               (6, 9, 1),
               )
cursor.execute("INSERT INTO map (house_id, x_value, y_value) VALUES (?, ?, ?)",
               (7, 1, 7),
               )
cursor.execute("INSERT INTO map (house_id, x_value, y_value) VALUES (?, ?, ?)",
               (8, 7, 3),
               )
cursor.execute("INSERT INTO map (house_id, x_value, y_value) VALUES (?, ?, ?)",
               (9, 8, 8),
               )
cursor.execute("INSERT INTO map (house_id, x_value, y_value) VALUES (?, ?, ?)",
               (10, 4, 6),
               )
# Commit and close
conn.commit()
conn.close()

import sqlite3

conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

# Delete all data from tables but keep structure
cursor.execute("DELETE FROM schedule;")
cursor.execute("DELETE FROM map;")

# Reset auto-increment counter (optional)
cursor.execute("DELETE FROM sqlite_sequence WHERE name='schedule';")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='map';")

conn.commit()
conn.close()

print("Database tables have been cleared.")

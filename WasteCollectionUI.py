import tkinter as tk
import sqlite3
import time
from threading import Thread

GRID_SIZE = 10
TRUCKS = {"Garbage": "red", "Recycling": "green", "Organic": "brown"}
BASE_LOCATION = (GRID_SIZE // 2, GRID_SIZE // 2)
CELL_SIZE = 50
WEEK_DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

class WasteCollectionUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚛 Smart Garbage Collection System")

        # Header
        self.header = tk.Label(root, text="Smart Garbage Collection Tracker", font=("Arial", 14, "bold"),
                               bg="lightgray", padx=10, pady=5)
        self.header.pack(fill=tk.X)

        # Layout Frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        # Canvas
        self.canvas = tk.Canvas(self.main_frame, width=GRID_SIZE * CELL_SIZE,
                                height=GRID_SIZE * CELL_SIZE, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        # Schedule Panel
        self.schedule_text = tk.Text(self.main_frame, width=60, height=20, font=("Arial", 10))
        self.schedule_text.pack(side=tk.RIGHT, padx=10)
        self.schedule_text.insert(tk.END, "📅 Weekly Waste Collection Schedule:\n")

        # Log Panel
        self.log_text = tk.Text(self.main_frame, width=40, height=20, font=("Arial", 10))
        self.log_text.pack(side=tk.RIGHT, padx=10)
        self.log_text.insert(tk.END, "🚛 Truck Activity Log:\n")

        # Load data
        self.houses = self.load_houses_from_db()
        self.schedule = self.load_schedule_from_db()

        # Draw layout
        self.draw_grid()
        self.draw_houses()
        self.display_schedule()

        # Truck icon
        self.truck_icon = self.canvas.create_text(BASE_LOCATION[0] * CELL_SIZE + 25,
                                                  BASE_LOCATION[1] * CELL_SIZE + 25,
                                                  text="🚛", font=("Arial", 16, "bold"))

        # Start scheduler simulation
        self.truck_thread = Thread(target=self.schedule_trucks, daemon=True)
        self.truck_thread.start()

    def load_houses_from_db(self):
        """Load only houses from the map table that are also scheduled."""
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()

        # Get house IDs from schedule
        cursor.execute("SELECT DISTINCT house_id FROM schedule")
        scheduled_ids = set(row[0] for row in cursor.fetchall())

        # Get house locations
        houses = {}
        for house_id in scheduled_ids:
            cursor.execute("SELECT x_value, y_value FROM map WHERE house_id = ?", (house_id,))
            result = cursor.fetchone()
            if result:
                x, y = result
                houses[house_id] = {"location": (x, y)}

        conn.close()
        return houses

    def load_schedule_from_db(self):
        """Loads actual weekly schedule from the schedule table."""
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM schedule")
        rows = cursor.fetchall()
        conn.close()

        schedule = {}
        for row in rows:
            request_id, house_id, truck_types, days = row
            truck_list = truck_types.split(", ")
            day_list = days.split(", ")
            schedule.setdefault(house_id, {})
            for t, d in zip(truck_list, day_list):
                schedule[house_id][t] = d
        return schedule

    def draw_grid(self):
        for i in range(GRID_SIZE + 1):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, GRID_SIZE * CELL_SIZE, fill="gray")
            self.canvas.create_line(0, i * CELL_SIZE, GRID_SIZE * CELL_SIZE, i * CELL_SIZE, fill="gray")

        # Draw base
        bx, by = BASE_LOCATION
        self.canvas.create_rectangle(bx * CELL_SIZE, by * CELL_SIZE,
                                     (bx + 1) * CELL_SIZE, (by + 1) * CELL_SIZE,
                                     fill="black")
        self.canvas.create_text(bx * CELL_SIZE + 25, by * CELL_SIZE + 25,
                                text="Base", fill="white", font=("Arial", 10, "bold"))

    def draw_houses(self):
        for house_id, data in self.houses.items():
            x, y = data["location"]
            self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                         (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                                         fill="blue")
            self.canvas.create_text(x * CELL_SIZE + 25, y * CELL_SIZE + 20,
                                    text=f"House {house_id}", fill="white", font=("Arial", 9, "bold"))

    def display_schedule(self):
        for house_id, waste_schedule in self.schedule.items():
            text = f"House {house_id}: " + ", ".join([f"{waste} on {day}" for waste, day in waste_schedule.items()])
            self.schedule_text.insert(tk.END, text + "\n")

    def move_truck(self, start, end):
        sx, sy = start
        ex, ey = end
        while (sx, sy) != (ex, ey):
            time.sleep(0.2)
            if sx < ex: sx += 1
            elif sx > ex: sx -= 1
            elif sy < ey: sy += 1
            elif sy > ey: sy -= 1

            self.canvas.coords(self.truck_icon, sx * CELL_SIZE + 25, sy * CELL_SIZE + 25)
            self.root.update_idletasks()

        time.sleep(0.5)
        return (sx, sy)

    def schedule_trucks(self):
        """Send trucks strictly based on the schedule table."""
        current_day_index = 0
        while True:
            current_day = WEEK_DAYS[current_day_index]
            self.log_text.insert(tk.END, f"\n📅 Today is {current_day}\n")
            self.log_text.see(tk.END)

            for house_id, house_data in self.houses.items():
                if house_id not in self.schedule:
                    continue

                scheduled_waste = self.schedule[house_id]

                for waste_type, scheduled_day in scheduled_waste.items():
                    if scheduled_day == current_day:
                        self.log_collection(house_id, waste_type, scheduled_day)
                        location = house_data["location"]
                        self.canvas.itemconfig(self.truck_icon, fill=TRUCKS[waste_type])
                        self.move_truck(BASE_LOCATION, location)
                        self.move_truck(location, BASE_LOCATION)

            # Go to next day every 5 seconds
            current_day_index = (current_day_index + 1) % len(WEEK_DAYS)
            time.sleep(5)

    def log_collection(self, house_id, waste_type, day):
        msg = f"🚛 {waste_type} truck sent to House {house_id} on {day}\n"
        self.log_text.insert(tk.END, msg)
        self.log_text.see(tk.END)

# Run the UI
if __name__ == "__main__":
    root = tk.Tk()
    app = WasteCollectionUI(root)
    root.mainloop()

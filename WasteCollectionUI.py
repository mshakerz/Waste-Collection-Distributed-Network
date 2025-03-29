import tkinter as tk
import sqlite3
import time
from threading import Thread

# Initializations
GRID_SIZE = 10 # 10x10 grid for neighbourhood
TRUCKS = {"Garbage": "red", "Recycling": "blue", "Organic": "green"} # dictionary for truck waste type and color
BASE_LOCATION = (GRID_SIZE // 2, GRID_SIZE // 2) # base location (middle of grid)
CELL_SIZE = 50 # pixel size of each cell
WEEK_DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

""" UI Class """
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

        # Right Panel (breaking up mainframe for schedule and activity log)
        self.right_panel = tk.Frame(self.main_frame)
        self.right_panel.pack(side=tk.RIGHT, padx=10)

        # Legend
        self.legend_frame = tk.Frame(self.right_panel)
        self.legend_frame.pack(side=tk.TOP, pady=30)

        # Schedule Panel
        self.schedule_text = tk.Text(self.right_panel, width=45, height=20, font=("Arial", 10))
        self.schedule_text.pack(side=tk.LEFT, padx=10)
        self.schedule_text.tag_configure('center', justify='center')
        self.schedule_text.insert(tk.END, "📅 Weekly Waste Collection Schedule:\n\n", 'center')

        # Log Panel
        self.log_text = tk.Text(self.right_panel, width=40, height=20, font=("Arial", 10))
        self.log_text.pack(side=tk.RIGHT, padx=10)
        self.log_text.insert(tk.END, "🚛 Truck Activity Log:\n", 'center')

        # Load map and schedule data
        self.houses = self.load_houses_from_db()
        self.schedule = self.load_schedule_from_db()

        # Draw layout
        self.draw_grid()
        self.draw_houses()
        self.draw_legend()
        self.display_schedule()

        # Create separate truck icons for each waste type
        self.truck_icons = {}
        for truck_type, color in TRUCKS.items():

            icon = self.canvas.create_text(BASE_LOCATION[0] * CELL_SIZE + 25,
                                           BASE_LOCATION[1] * CELL_SIZE + 25,
                                           text="🚛", font=("Arial", 16, "bold"),
                                           fill=color)
            self.truck_icons[truck_type] = icon

        # Start scheduler simulation
        self.truck_thread = Thread(target=self.schedule_trucks, daemon=True)
        self.truck_thread.start()

    """ Loads map from DB """
    def load_houses_from_db(self):
        # Loads house positions for all houses in neighbourhood
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()

        # Get all house locations
        cursor.execute("SELECT house_id, x_value, y_value FROM map")
        houses = {}
        for row in cursor.fetchall():
            house_id, x, y = row
            houses[house_id] = {"location": (x, y)}

        conn.close()
        return houses

    """ Load schedule from DB"""
    def load_schedule_from_db(self):
        # Loads all house sched entries from schedule table
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM schedule")
        rows = cursor.fetchall()
        conn.close()

        # Converting rows to dictionary format
        schedule = {}
        for row in rows:
            request_id, house_id, truck_types, days = row
            truck_list = truck_types.split(", ")
            day_list = days.split(", ")
            schedule.setdefault(house_id, {})
            for t, d in zip(truck_list, day_list):
                schedule[house_id][t] = d
        return schedule

    """ Draws 10x10 grid and highlight base """
    def draw_grid(self):
        for i in range(GRID_SIZE + 1):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, GRID_SIZE * CELL_SIZE, fill="gray")
            self.canvas.create_line(0, i * CELL_SIZE, GRID_SIZE * CELL_SIZE, i * CELL_SIZE, fill="gray")

        # Draw base (center of grid)
        bx, by = BASE_LOCATION
        self.canvas.create_rectangle(bx * CELL_SIZE, by * CELL_SIZE,
                                     (bx + 1) * CELL_SIZE, (by + 1) * CELL_SIZE,
                                     fill="black")
        self.canvas.create_text(bx * CELL_SIZE + 25, by * CELL_SIZE + 25,
                                text="Base", fill="white", font=("Arial", 10, "bold"))

    """ Draws houses on map grid"""
    def draw_houses(self):
        for house_id, data in self.houses.items():
            x, y = data["location"]
            self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                         (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                                         fill="grey")
            self.canvas.create_text(x * CELL_SIZE + 25, y * CELL_SIZE + 20,
                                    text=f"House {house_id}", fill="white", font=("Arial", 9, "bold"))

    """ Draws legend for truck types"""
    def draw_legend(self):
        # Legend label
        legend_label = tk.Label(self.legend_frame, text="Truck Legend", font=("Arial", 12, "bold"))
        legend_label.pack(side=tk.TOP, pady=5)

        for i, (truck_type, color) in enumerate(TRUCKS.items()):
            # legend colored boxes
            boxes = tk.Canvas(self.legend_frame, width=20, height=20, bg=color, bd=0)
            boxes.pack(side=tk.LEFT, padx=5)
            # type label
            label = tk.Label(self.legend_frame, text=truck_type, font=("Arial", 10))
            label.pack(side=tk.LEFT, padx=5)

    """ Displays daily schedule of houses to visit by waster type"""
    def display_schedule(self):
        # day -> waste type -> houses
        schedule_data = {day: {t: [] for t in TRUCKS} for day in WEEK_DAYS}

        for house_id, waste_schedule in self.schedule.items():
            for waste_type, day in waste_schedule.items():
                if day in schedule_data and waste_type in TRUCKS:
                    schedule_data[day][waste_type].append(house_id)

        # Create chart to display schedule
        for day in WEEK_DAYS:
            day_data = schedule_data[day]
            self.schedule_text.insert(tk.END, f"🗓 {day}\n", ("day",))
            for waste_type in TRUCKS:
                houses = day_data[waste_type]
                if houses:
                    house_list = ", ".join(f"House {h}" for h in sorted(houses))
                    text = f"   - {waste_type}: {house_list}\n"
                    self.schedule_text.insert(tk.END, text, waste_type)
                self.schedule_text.insert(tk.END, "\n")

    """ Animates truck movement along scheduled path"""
    def move_truck(self, truck_icon, path):
        for (x, y) in path:
            self.canvas.coords(truck_icon, x * CELL_SIZE + 25, y * CELL_SIZE + 25)
            self.root.update_idletasks()
            time.sleep(0.5)
        time.sleep(0.5)

    """ Loops one day at a time to dispatch truck"""
    def schedule_trucks(self):
        """Send trucks strictly based on the schedule table."""
        current_day_index = 0
        while True:
            current_day = WEEK_DAYS[current_day_index]
            self.log_text.tag_configure('center', justify='center')
            self.log_text.insert(tk.END, f"\n📅 Today is {current_day}\n", 'center')
            self.log_text.see(tk.END)

            for truck_type in TRUCKS:
                # Get all houses scheduled for the given type on the selected day
                stops = []
                for house_id, waste_type in self.schedule.items():
                    if waste_type.get(truck_type) == current_day:
                        loc = self.houses[house_id]["location"]
                        stops.append((house_id, loc))

                if stops:
                    self.dispatch_truck(truck_type, stops, current_day)
                # delay between trucks
                time.sleep(1.5)

            # Go to next day every 3 seconds
            current_day_index = (current_day_index + 1) % len(WEEK_DAYS)
            time.sleep(3)

    """ Dispatches required truck after building path based on schedule, returning to base"""
    def dispatch_truck(self, truck_type, stops, day):
        truck_icon = self.truck_icons[truck_type]
        current_position = BASE_LOCATION
        path = []

        # Creating the path without using log_collection
        for _, loc in stops:
            # move from current position to house
            path += self.get_path(current_position, loc)
            current_position = loc

        # Return to base
        path += self.get_path(current_position, BASE_LOCATION)
        # Move truck
        self.move_truck(truck_icon, path)

        # Log after returning to base
        for house_id, _ in stops:
            self.log_collection(house_id, truck_type, day)

    """ Calculates path between two points (in a straight line to mimic city streets)"""
    def get_path(self, start, end):
        path = []
        sx, sy = start
        ex, ey = end

        while sx != ex:
            if sx < ex:
                sx += 1
            else:
                sx -= 1
            path.append((sx, sy))

        while sy != ey:
            if sy < ey:
                sy += 1
            else:
                sy -= 1
            path.append((sx, sy))

        return path

    """ Adds truck activity to log panel once truck completes route """
    def log_collection(self, house_id, waste_type, day):
        msg = f"🚛 {waste_type} truck sent to House {house_id} on {day}\n"
        self.log_text.insert(tk.END, msg)
        self.log_text.see(tk.END)

# Run the UI
if __name__ == "__main__":
    root = tk.Tk()
    app = WasteCollectionUI(root)
    root.mainloop()

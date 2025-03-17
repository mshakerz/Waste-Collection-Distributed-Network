import tkinter as tk
import random
import time
from threading import Thread

GRID_SIZE = 10
HOUSE_COUNT = 10
TRUCKS = {"Garbage": "red", "Recycling": "green", "Organic": "brown"}  # Truck colors
THRESHOLD = 80  # Waste percentage threshold
BASE_LOCATION = (GRID_SIZE // 2, GRID_SIZE // 2)  # Base is at the center
CELL_SIZE = 50  # Size of each cell in pixels
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

class WasteCollectionUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Waste Collection Scheduler")

        # Header Label
        self.header = tk.Label(root, text="🚛 Welcome to the Waste Collection Scheduler 🚛",
                               font=("Arial", 14, "bold"), bg="lightgray", padx=10, pady=5)
        self.header.pack(fill=tk.X)

        # Create main layout frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        # Create canvas for the grid
        self.canvas = tk.Canvas(self.main_frame, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        # Create log panel
        self.log_text = tk.Text(self.main_frame, width=40, height=15, font=("Arial", 10))
        self.log_text.pack(side=tk.RIGHT, padx=10, pady=10)
        self.log_text.insert(tk.END, "Waste Collection Log:\n")

        # Create schedule panel
        self.schedule_text = tk.Text(self.main_frame, width=80, height=15, font=("Arial", 10))
        self.schedule_text.pack(side=tk.RIGHT, padx=10, pady=10)
        self.schedule_text.insert(tk.END, "Weekly Waste Collection Schedule:\n")

        # Generate houses & schedules
        self.houses = self.generate_houses()
        self.schedule = self.generate_schedule()

        # Draw grid, houses, and base station
        self.draw_grid()
        self.draw_houses()
        self.display_schedule()

        # Create truck icon
        self.truck_icon = self.canvas.create_text(BASE_LOCATION[0] * CELL_SIZE + 25,
                                                  BASE_LOCATION[1] * CELL_SIZE + 25,
                                                  text="🚛", font=("Arial", 16, "bold"))

        # Start truck scheduler in a separate thread
        self.truck_thread = Thread(target=self.schedule_trucks, daemon=True)
        self.truck_thread.start()

    def generate_houses(self):
        """Generate random house locations and waste percentages."""
        houses = {}
        used_locations = set()

        for house_id in range(1, HOUSE_COUNT + 1):
            while True:
                x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
                if (x, y) not in used_locations and (x, y) != BASE_LOCATION:
                    used_locations.add((x, y))
                    break

            waste_percentages = {waste_type: random.randint(10, 90) for waste_type in TRUCKS.keys()}
            houses[house_id] = {
                "location": (x, y),
                "waste": waste_percentages
            }

        return houses

    def generate_schedule(self):
        """Generate a weekly schedule for waste collection per house."""
        schedule = {}
        for house_id in range(1, HOUSE_COUNT + 1):
            schedule[house_id] = {waste_type: random.choice(WEEK_DAYS) for waste_type in TRUCKS.keys()}
        return schedule

    def draw_grid(self):
        """Draw a 10x10 grid on the canvas."""
        for i in range(GRID_SIZE + 1):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, GRID_SIZE * CELL_SIZE, fill="gray")
            self.canvas.create_line(0, i * CELL_SIZE, GRID_SIZE * CELL_SIZE, i * CELL_SIZE, fill="gray")

        # Draw Base (Garbage dump)
        bx, by = BASE_LOCATION
        self.canvas.create_rectangle(
            bx * CELL_SIZE, by * CELL_SIZE,
            (bx + 1) * CELL_SIZE, (by + 1) * CELL_SIZE,
            fill="black"
        )
        self.canvas.create_text(
            bx * CELL_SIZE + 25, by * CELL_SIZE + 25,
            text="Base", fill="white", font=("Arial", 10, "bold")
        )

    def draw_houses(self):
        """Draw houses on the grid with labels."""
        for house_id, house_data in self.houses.items():
            x, y = house_data["location"]
            self.canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                fill="blue"
            )
            self.canvas.create_text(
                x * CELL_SIZE + 25, y * CELL_SIZE + 20,
                text=f"House {house_id}", fill="white",
                font=("Arial", 9, "bold")
            )

    def display_schedule(self):
        """Display the weekly schedule for each house."""
        for house_id, days in self.schedule.items():
            schedule_text = f"House {house_id}: "
            schedule_text += ", ".join([f"{waste} on {day}" for waste, day in days.items()])
            self.schedule_text.insert(tk.END, schedule_text + "\n")

    def move_truck(self, start, end):
        """Move the truck from the base to a house step by step."""
        sx, sy = start
        ex, ey = end
        while (sx, sy) != (ex, ey):
            time.sleep(0.3)
            if sx < ex:
                sx += 1
            elif sx > ex:
                sx -= 1
            elif sy < ey:
                sy += 1
            elif sy > ey:
                sy -= 1

            self.canvas.coords(self.truck_icon, sx * CELL_SIZE + 25, sy * CELL_SIZE + 25)
            self.root.update_idletasks()

        time.sleep(1)
        return (sx, sy)

    def schedule_trucks(self):
        """Simulate truck scheduling and collection."""
        while True:
            time.sleep(3)
            for house_id, house_data in self.houses.items():
                for waste_type, percentage in house_data["waste"].items():
                    if percentage >= THRESHOLD:
                        self.log_collection(house_id, waste_type)
                        house_location = house_data["location"]
                        self.canvas.itemconfig(self.truck_icon, fill=TRUCKS[waste_type])

                        self.move_truck(BASE_LOCATION, house_location)
                        self.houses[house_id]["waste"][waste_type] = 0
                        self.move_truck(house_location, BASE_LOCATION)

    def log_collection(self, house_id, waste_type):
        """Log truck collection events."""
        log_message = f"🚛 House {house_id}: {waste_type} Truck Sent\n"
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)


# Run the UI
if __name__ == "__main__":
    root = tk.Tk()
    app = WasteCollectionUI(root)
    root.mainloop()

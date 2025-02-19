import csv
import datetime
import keyboard  # Requires installation: pip install keyboard
import tkinter as tk
from tkinter import messagebox

def get_user_input(prompt):
    """Helper function to get user input with validation."""
    return input(prompt).strip()

def keyboard_tally_counter():
    """Function to count vehicles using keyboard shortcuts."""
    counts = {"right": 0, "through": 0, "left": 0}
    print("Start tallying. Press 'R' for right turns, 'T' for through, 'L' for left turns. Press 'D' when done.")

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'r':
                counts["right"] += 1
                print(f"Right Turns: {counts['right']}")
            elif event.name == 't':
                counts["through"] += 1
                print(f"Vehicles Through: {counts['through']}")
            elif event.name == 'l':
                counts["left"] += 1
                print(f"Left Turns: {counts['left']}")
            elif event.name == 'd':
                keyboard.clear_all_hotkeys()  # Clear the keyboard event buffer
                break
    
    return counts["right"], counts["through"], counts["left"]

def collect_traffic_data():
    """Function to collect traffic observation data and save to a CSV file."""
    file_name = "traffic_observations.csv"
    
    # Define CSV headers
    headers = [
        "Time Interval", "Weather", "Detection Zone Stuck", "Detection Zones Changing Color", 
        "Vehicles Turned Right", "Vehicles Went Through", "Vehicles Turned Left", "Camera Name"
    ]
    
    # Open the file and check if headers exist
    try:
        with open(file_name, "r") as f:
            pass  # File exists, do nothing
    except FileNotFoundError:
        # Create file and write headers if it doesn't exist
        with open(file_name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    # GUI for data collection
    root = tk.Tk()
    root.title("Traffic Data Collection")

    def validate_weather():
        valid_conditions = ["Sunny", "Cold", "Hot", "Warm"]
        weather = weather_entry.get()
        if weather not in valid_conditions:
            messagebox.showerror("Invalid Input", "Please enter a valid weather condition: Sunny, Cold, Hot, Warm.")
            return False
        return True

    def submit_data():
        if not validate_weather():
            return
        
        # Get the current time interval
        start_time = datetime.datetime.now().strftime("%I:%M %p")
        end_time = (datetime.datetime.now() + datetime.timedelta(minutes=15)).strftime("%I:%M %p")
        time_interval = f"{start_time} - {end_time}"

        # Collect observations
        weather = weather_entry.get()
        detection_zone_stuck = stuck_var.get()
        detection_zone_changing = changing_var.get()
        
        # Use keyboard tally system for vehicle counts
        vehicles_right, vehicles_through, vehicles_left = keyboard_tally_counter()

        # Save data to CSV file
        with open(file_name, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                time_interval, weather, detection_zone_stuck, detection_zone_changing, 
                vehicles_right, vehicles_through, vehicles_left, camera_name_entry.get()
            ])
        
        messagebox.showinfo("Success", "Data recorded successfully!")
        
        # Clear inputs for next entry
        weather_entry.delete(0, tk.END)
        camera_name_entry.delete(0, tk.END)

    # GUI Elements
    tk.Label(root, text="Weather Condition:").pack()
    weather_entry = tk.Entry(root)
    weather_entry.pack()

    tk.Label(root, text="Is the detection zone stuck?").pack()
    stuck_var = tk.StringVar(value="No")
    tk.Radiobutton(root, text="Yes", variable=stuck_var, value="Yes").pack()
    tk.Radiobutton(root, text="No", variable=stuck_var, value="No").pack()

    tk.Label(root, text="Are the detection zones changing color?").pack()
    changing_var = tk.StringVar(value="No")
    tk.Radiobutton(root, text="Yes", variable=changing_var, value="Yes").pack()
    tk.Radiobutton(root, text="No", variable=changing_var, value="No").pack()

    tk.Label(root, text="Camera Name:").pack()
    camera_name_entry = tk.Entry(root)
    camera_name_entry.pack()

    tk.Button(root, text="Submit Data", command=submit_data).pack()

    root.mainloop()

if __name__ == "__main__":
    collect_traffic_data()

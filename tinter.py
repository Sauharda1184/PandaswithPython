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
    counts = {"u_turn": 0, "left": 0, "through": 0, "right": 0, "pedestrians": 0}
    print("Start tallying. Press 'Q' for U turns, 'W' for left turns, 'E' for vehicles through, 'R' for right turns, 'T' for pedestrians. Press 'D' when done.")

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'q':
                counts["u_turn"] += 1
                print(f"U Turns: {counts['u_turn']}")
            elif event.name == 'w':
                counts["left"] += 1
                print(f"Left Turns: {counts['left']}")
            elif event.name == 'e':
                counts["through"] += 1
                print(f"Vehicles Through: {counts['through']}")
            elif event.name == 'r':
                counts["right"] += 1
                print(f"Right Turns: {counts['right']}")
            elif event.name == 't':
                counts["pedestrians"] += 1
                print(f"Pedestrians: {counts['pedestrians']}")
            elif event.name == 'd':
                keyboard.clear_all_hotkeys()  # Clear the keyboard event buffer
                print("Tallying done.")
                break  # Exit the loop when 'D' is pressed

    return counts["right"], counts["through"], counts["left"], counts["u_turn"], counts["pedestrians"]

def get_weather_input():
    valid_conditions = ["Sunny", "Cold", "Hot", "Warm"]
    while True:
        weather = get_user_input("Enter weather condition (Sunny, Cold, Hot, Warm, etc.): ")
        if weather in valid_conditions:
            return weather
        else:
            print("Invalid input. Please enter one of the following: Sunny, Cold, Hot, Warm.")

def collect_traffic_data():
    """Function to collect traffic observation data and save to a CSV file."""
    file_name = "traffic_observations.csv"
    
    # Define CSV headers
    headers = [
        "Time Interval", "Date", "Weather", "Detection Zone Stuck", "Detection Zones Changing Color", 
        "Vehicles Turned Right", "Vehicles Went Through", "Vehicles Turned Left", "U Turns", "Pedestrians", "Camera Name"
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

    # Use keyboard tally system for vehicle counts
    vehicles_right, vehicles_through, vehicles_left, vehicles_u_turn, vehicles_pedestrians = keyboard_tally_counter()

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
        
        # Get the time interval and date from user input
        time_interval = time_interval_entry.get()  # Format: "10:00:00 to 10:15:00"
        date = date_entry.get()  # Format: "mm/dd/yyyy"

        # Collect observations
        weather = weather_entry.get()
        detection_zone_stuck = stuck_var.get()
        detection_zone_changing = changing_var.get()
        
        # Save data to CSV file
        with open(file_name, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                time_interval, date, weather, detection_zone_stuck, detection_zone_changing, 
                vehicles_right, vehicles_through, vehicles_left, vehicles_u_turn, vehicles_pedestrians, camera_name_entry.get()
            ])
        
        messagebox.showinfo("Success", "Data recorded successfully!")
        
        # Clear inputs for next entry
        weather_entry.delete(0, tk.END)
        time_interval_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        camera_name_entry.delete(0, tk.END)

    # GUI Elements
    tk.Label(root, text="Time Interval (hh:mm:ss to hh:mm:ss):").pack()
    time_interval_entry = tk.Entry(root)
    time_interval_entry.pack()

    tk.Label(root, text="Date (mm/dd/yyyy):").pack()
    date_entry = tk.Entry(root)
    date_entry.pack()

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

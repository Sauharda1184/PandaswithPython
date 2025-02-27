import csv
import datetime
import keyboard  # Requires installation: pip install keyboard
import tkinter as tk
from tkinter import messagebox

def get_user_input(prompt):
    """Helper function to get user input with validation."""
    return input(prompt).strip()

def keyboard_tally_counter(direction):
    """Function to count vehicles using keyboard shortcuts for a specific direction."""
    counts = {"left": 0, "through": 0, "right": 0}
    direction_names = {
        "SB": "South Bound",
        "EB": "East Bound",
        "NB": "North Bound",
        "WB": "West Bound"
    }
    
    print(f"\nCounting for {direction_names[direction]} ({direction})")
    print("Press 'W' for left turns, 'E' for vehicles through, 'R' for right turns.")
    print("Press 'D' when done with this direction.")
    
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'w':
                counts["left"] += 1
                print(f"{direction} Left Turns: {counts['left']}")
            elif event.name == 'e':
                counts["through"] += 1
                print(f"{direction} Through: {counts['through']}")
            elif event.name == 'r':
                counts["right"] += 1
                print(f"{direction} Right Turns: {counts['right']}")
            elif event.name == 'd':
                print(f"Finished counting for {direction_names[direction]}.")
                break  # Exit the loop when 'D' is pressed
    
    return counts

def select_direction():
    """Function to select which direction to count for."""
    print("\nSelect direction to count:")
    print("1: South Bound (SB)")
    print("2: East Bound (EB)")
    print("3: North Bound (NB)")
    print("4: West Bound (WB)")
    print("5: Finish data collection")
    
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == '1':
                return "SB"
            elif event.name == '2':
                return "EB"
            elif event.name == '3':
                return "NB"
            elif event.name == '4':
                return "WB"
            elif event.name == '5':
                return None

def get_weather_input():
    valid_conditions = ["Sunny", "Cold", "Hot", "Warm", "Rainy", "Snowy"]
    while True:
        weather = get_user_input("Enter weather condition (Sunny, Cold, Hot, Warm, Rainy, Snowy etc.): ")
        if weather in valid_conditions:
            return weather
        else:
            print("Invalid input. Please enter one of the following: Sunny, Cold, Hot, Warm, Rainy, Snowy.")

def collect_traffic_data():
    """Function to collect traffic observation data and save to a CSV file."""
    file_name = "intersection_traffic_new.csv"
    
    # Define CSV headers
    headers = [
        "Time Interval", "Date", "Weather", "Detection Zone Stuck", "Detection Zones Changing Color",
        "SBR", "SBT", "SBL",
        "EBR", "EBT", "EBL",
        "NBR", "NBT", "NBL",
        "WBR", "WBT", "WBL",
        "Total Vehicles", "Camera Name"
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

    # Initialize counts for all directions
    direction_counts = {
        "SB": {"right": 0, "through": 0, "left": 0},
        "EB": {"right": 0, "through": 0, "left": 0},
        "NB": {"right": 0, "through": 0, "left": 0},
        "WB": {"right": 0, "through": 0, "left": 0}
    }
    
    print("Starting intersection traffic data collection.")
    print("You will be able to count for each direction separately.")
    
    # Collect data for each direction
    while True:
        direction = select_direction()
        if direction is None:
            break
        
        counts = keyboard_tally_counter(direction)
        direction_counts[direction]["right"] = counts["right"]
        direction_counts[direction]["through"] = counts["through"]
        direction_counts[direction]["left"] = counts["left"]
    
    # Calculate total vehicles
    total_vehicles = 0
    for direction in direction_counts:
        for movement in ["right", "through", "left"]:
            total_vehicles += direction_counts[direction][movement]
    
    # GUI for additional data collection
    root = tk.Tk()
    root.title("Intersection Traffic Data Collection")

    def validate_weather():
        valid_conditions = ["Sunny", "Cold", "Hot", "Warm", "Rainy", "Snowy"]
        weather = weather_entry.get()
        if weather not in valid_conditions:
            messagebox.showerror("Invalid Input", "Please enter a valid weather condition: Sunny, Cold, Hot, Warm, Rainy, Snowy.")
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
                direction_counts["SB"]["right"], direction_counts["SB"]["through"], direction_counts["SB"]["left"],
                direction_counts["EB"]["right"], direction_counts["EB"]["through"], direction_counts["EB"]["left"],
                direction_counts["NB"]["right"], direction_counts["NB"]["through"], direction_counts["NB"]["left"],
                direction_counts["WB"]["right"], direction_counts["WB"]["through"], direction_counts["WB"]["left"],
                total_vehicles, camera_name_entry.get()
            ])
        
        messagebox.showinfo("Success", "Data recorded successfully!")
        root.destroy()

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
    
           
   
 

      
   

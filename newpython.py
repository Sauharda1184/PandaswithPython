import csv
import datetime
import keyboard  # Requires installation: pip install keyboard
import pandas as pd

def get_user_input(prompt):
    """Helper function to get user input with validation."""
    return input(prompt).strip()

def keyboard_tally_counter():
    """Function to count vehicles using keyboard shortcuts at a 4-camera intersection with 15-minute intervals."""
    directions = ["EBL", "EBT", "EBR", "WBL", "WBT", "WBR", "NBL", "NBT", "NBR", "SBL", "SBT", "SBR"]
    counts = {dir: 0 for dir in directions}
    
    print("Start tallying. Use keys 1-4 to select direction (1: SB, 2: EB, 3: NB, 4: WB)")
    print("Then use 'Q' for U turns, 'W' for left turns, 'E' for through, 'R' for right. Press 'D' when done.")
    
    current_direction = "SB"
    start_time = datetime.datetime.now()
    interval = datetime.timedelta(minutes=15)
    
    while True:
        current_time = datetime.datetime.now()
        if (current_time - start_time) >= interval:
            break
        
        if keyboard.is_pressed('1'):
            current_direction = "SB"
            print("Now recording for South Bound (SB)")
        elif keyboard.is_pressed('2'):
            current_direction = "EB"
            print("Now recording for East Bound (EB)")
        elif keyboard.is_pressed('3'):
            current_direction = "NB"
            print("Now recording for North Bound (NB)")
        elif keyboard.is_pressed('4'):
            current_direction = "WB"
            print("Now recording for West Bound (WB)")
        elif keyboard.is_pressed('q'):
            counts[f"{current_direction}L"] += 1
        elif keyboard.is_pressed('w'):
            counts[f"{current_direction}B"] += 1
        elif keyboard.is_pressed('e'):
            counts[f"{current_direction}T"] += 1
        elif keyboard.is_pressed('r'):
            counts[f"{current_direction}R"] += 1
        elif keyboard.is_pressed('d'):
            print("Exiting data collection...")
            break
    
    return counts

def save_to_csv(counts, intersection_name):
    """Save traffic data to CSV file in the specified format."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{intersection_name}_traffic_data_{timestamp}.csv"
    
    df = pd.DataFrame([counts])
    df.insert(0, "Time", datetime.datetime.now().strftime("%H:%M"))
    df.to_csv(filename, index=False)
    
    print(f"Traffic data saved to {filename}")

def main():
    intersection_name = get_user_input("Enter intersection name: ")
    counts = keyboard_tally_counter()
    save_to_csv(counts, intersection_name)
    print("Data collection complete.")

if __name__ == "__main__":
    main()

          

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
    counts = {dir: [] for dir in directions}
    
    print("Start tallying. Use keys 1-4 to select direction (1: SB, 2: EB, 3: NB, 4: WB)")
    print("Then use 'Q' for U turns, 'W' for left turns, 'E' for through, 'R' for right. Press 'D' when done.")
    
    start_time = datetime.datetime.now()
    interval = datetime.timedelta(minutes=15)
    
    while True:
        current_time = datetime.datetime.now()
        if (current_time - start_time) >= interval:
            break
        
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'q':
                counts["EBL"].append(1)
            elif event.name == 'w':
                counts["WBL"].append(1)
            elif event.name == 'e':
                counts["NBT"].append(1)
            elif event.name == 'r':
                counts["SBT"].append(1)
            elif event.name == 'd':
                break
    
    for key in counts:
        counts[key] = sum(counts[key])
    
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

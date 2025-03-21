# DATA ANALYSIS WITH PANDAS (PYTHON)

## DESCRIPTION
Completed a comprehensive data analysis project as part of Corey Schafer's YouTube course, leveraging Python libraries such as Pandas, Matplotlib, Seaborn, and NumPy. The project involved cleaning and preprocessing raw datasets, performing exploratory data analysis (EDA) to uncover trends and insights, and visualizing key findings using effective charts and graphs. Applied statistical techniques to draw meaningful conclusions and presented data-driven insights in a structured manner.

## TECHNOLOGIES USED
Python, Pandas, NumPy, Matplotlib, Seaborn, Jupyter Notebook

## function 
Okay, let's see. I need to explain this program in simple terms. The user provided a Python script called apiImport.py. Let me read through it first.

The program starts by importing various libraries like tkinter for the GUI, requests for web requests, pandas for data handling, and others. Then there's a class App which seems to create a GUI window. The __init__ method sets up the window with labels, entry fields, buttons, and a checkbox. The clear_button_command resets all the input fields. The Submit_button_command is where most of the action happens when the user clicks submit.

Looking at the Submit function, it does several things. It gets the user inputs like the filename, IP address, start and end dates. Then it validates these inputs. For the IP address, it checks the format, length, and correct octet values. For the dates, it ensures they are in the right format and logical (end date not before start, etc.). If there's a bypass checkbox checked, maybe it skips some errors?

After validation, there's a function to convert time zones. Then, the program constructs a URL using the IP and dates to fetch data from an API. It uses requests and BeautifulSoup to parse the data. It seems to loop through camera directions (1 to 4), gets data for each, processes it with pandas, cleans the data, and combines data from all cameras.

The data processing includes splitting columns, renaming them, cleaning strings, handling time zones, and aggregating data into 15-minute intervals. Finally, it generates a summary CSV file with traffic data like left, through, right turns for each direction, and total vehicles.

The program also handles errors, like if the IP is unreachable or data is missing, showing status messages. The GUI updates the user with these statuses.

So, in simple terms, this program is a GUI application that lets users input details about a traffic intersection's IP and date range. It fetches traffic data from that IP via an API, processes the data, and outputs a CSV summary. The checks ensure valid inputs, and the bypass option might skip some errors to continue processing.

This program is a traffic data collector that fetches and processes information from traffic cameras via a user-friendly interface. Here's how it works:

What It Does:

User Interface:
Opens a window where you enter:
A file name (to save data).
An IP address (e.g., 192.168.xxx.xxx for the traffic cameras).
Start and end dates (to specify the data range).
Buttons:
Clear: Resets all fields.
Submit: Starts data collection.
Bypass Checkbox: Skips some errors (use carefully).
Validation:
Checks if inputs are correct:
IP address format (e.g., valid numbers, periods, length).
Dates (valid format, logical range).
Filename (not empty).
Shows error messages (e.g., "IP too short" or "Invalid date") if something’s wrong.
Data Fetching:
Connects to the traffic cameras via the IP address.
Fetches traffic statistics (speed, volume, turns) from 4 directional cameras (North, South, East, West).
Data Processing:
Cleans and organizes raw data.
Converts timestamps to your local time zone.
Splits data into 15-minute intervals for analysis.
Removes unnecessary details (like bike lanes or advanced detectors).
Output:
Generates a CSV file with summarized traffic data:
Vehicle counts (left/through/right turns) for each direction.
Total vehicles per time interval.
How It Works:

GUI: Built with tkinter for buttons, labels, and input fields.
Web Requests: Uses requests and BeautifulSoup to fetch and parse API data.
Data Handling: Uses pandas to clean, sort, and analyze data.
Time Zones: Converts timestamps using pytz for accuracy.
Key Features:

Error Handling: Guides users to fix mistakes (e.g., invalid IP or dates).
Bypass Option: Skips problematic cameras to continue processing (may affect data).
Automated Formatting: Ensures dates and IPs are correctly structured.
In short, this program simplifies collecting traffic data from cameras, validates inputs, and delivers a clean, summarized report. 🚦📊

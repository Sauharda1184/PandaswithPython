# Imports all packages used in the program.
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import date
import subprocess as s
import time
import os
import tempfile
import shutil
import uuid
import sys

def get_excel_path():
    # First try the command line argument
    if len(sys.argv) > 1:
        return sys.argv[1]
    
    # Then try the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(script_dir, 'HC TMC Asset Tracking - February.xlsx'),
        os.path.join(script_dir, 'Asset Tracking.xlsx'),
        os.path.join(os.path.dirname(script_dir), 'HC TMC Asset Tracking - February.xlsx')
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # If no file is found, ask the user
    print("\nExcel file not found. Please enter the full path to your Excel file:")
    print("(Example: C:\\Users\\YourName\\Desktop\\HC TMC Asset Tracking - February.xlsx)")
    user_path = input("Excel file path: ").strip('"').strip("'")
    
    if os.path.exists(user_path):
        return user_path
    else:
        raise FileNotFoundError(f"Could not find the Excel file at: {user_path}")

try:
    # Get the Excel file path
    excel_path = get_excel_path()
    print(f"Using Excel file: {excel_path}")

    # Reads the Asset Tracking sheet
    df = pd.read_excel(excel_path, sheet_name="Asset Tracking", usecols="A, C, H, M")
    df = df.dropna(axis=0)
    df = df.rename(columns=df.iloc[0]).drop(df.index[0])

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Setup ChromeDriver path
    chromedriver_path = os.path.join(script_dir, 'chromedriver.exe')

    # Set up Chrome options
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Create a temporary directory
    temp_dir = os.path.join(tempfile.gettempdir(), f'chrome_temp_{uuid.uuid4().hex}')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    options.add_argument(f'--user-data-dir={temp_dir}')

    # Initialize the Chrome WebDriver with explicit service
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    # Run on only Vision intersections
    vision = df[df["Detection Type"].str.contains("Vision")]

    # Uses intersection and ip_address to get screenshots
    id = list(vision["ID"])
    intersection = list(vision["Intersection"])
    ip_address = list(vision["Tap/Detection IP"])

    log = []
    results = []

    # Determines current date, to append to the file name
    today = pd.to_datetime(date.today())
    today = str(today)
    today = today.split(" ")
    today = str(today[0])

    # Create output directory if it doesn't exist
    output_dir = os.path.join(script_dir, 'screenshots')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Filler value to use to iterate
    i = 0

    while i < len(ip_address):
        # Sets the ip address, and what to name the screenshot
        url_format = "http://" + ip_address[i] + "/api/v1/snapshot?timestamp=n&jpeg-quality=100"
        intersection_name = str(id[i]) + " " + intersection[i] + " " + str(today) + " Vision" + ".png"
        # Make sure the filename is valid for Windows
        intersection_name = "".join(c for c in intersection_name if c not in '<>:"/\\|?*')

        # Opens the website
        try:
            time.sleep(5)
            driver.get(url_format)
            screenshot_path = os.path.join(output_dir, intersection_name)
            driver.save_screenshot(screenshot_path)
            result = "Success"
            print(f"Successfully captured: {intersection[i]}")
        except Exception as e:
            result = "Failure"
            print(f"Error at {intersection[i]}: {str(e)}")

        log.append(([id[i], intersection[i], ip_address[i], result]))
        results = pd.DataFrame(log, columns=["ID", "Intersection Name", "IP Address", "Result"])
        i = i + 1

    # Save results with full path
    log_file = os.path.join(output_dir, f"Vision Screenshot Log {today}.csv")
    results.to_csv(log_file)
    print(f"\nProcess completed. Results saved to: {log_file}")

except Exception as e:
    print(f"\nAn error occurred: {str(e)}")
    print("Please make sure:")
    print("1. The Excel file exists and is accessible")
    print("2. The Excel file has the correct sheet name 'Asset Tracking'")
    print("3. The required columns (A, C, H, M) exist in the sheet")
    sys.exit(1)

finally:
    # Clean up
    try:
        if 'driver' in locals():
            driver.quit()
    except:
        pass
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

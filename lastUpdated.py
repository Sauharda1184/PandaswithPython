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

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Setup ChromeDriver path (assuming chromedriver.exe is in the same directory as the script)
chromedriver_path = os.path.join(script_dir, 'chromedriver.exe')

# Reads the Asset Tracking sheet, stored in the same directory as the program
excel_path = os.path.join(script_dir, 'HC TMC Asset Tracking - February.xlsx')
df = pd.read_excel(excel_path, sheet_name="Asset Tracking", usecols="A, C, H, M")
df = df.dropna(axis=0)
df = df.rename(columns=df.iloc[0]).drop(df.index[0])

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

try:
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
            driver.save_screenshot(os.path.join(script_dir, intersection_name))
            result = "Success"
        except Exception as e:
            result = "Failure"
            print(f"Error at {intersection[i]}: {str(e)}")

        log.append(([id[i], intersection[i], ip_address[i], result]))
        results = pd.DataFrame(log, columns=["ID", "Intersection Name", "IP Address", "Result"])
        i = i + 1

    # Save results with full path
    results.to_csv(os.path.join(script_dir, f"Vision Screenshot Log {today}.csv"))

finally:
    # Clean up
    try:
        driver.quit()
    except:
        pass
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

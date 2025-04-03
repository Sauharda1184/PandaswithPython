# Imports all packages used in the program.
import pandas as pd
from selenium import webdriver
from datetime import date
import subprocess as s
import time

# Reads the Asset Tracking sheet, stored in the same directory as the program
df = pd.read_excel('HC TMC Asset Tracking - February.xlsx', sheet_name="Asset Tracking", usecols="A, C, H, M")
df = df.dropna(axis=0)
df = df.rename(columns=df.iloc[0]).drop(df.index[0])

# Designates Chrome as the browser our links will open in.
driver = webdriver.Chrome()

# Run on only Vision intersections
vision = df[df["Detection Type"].str.contains("Vision")]

# Uses intersection and ip_address to get screenshots
id = list(vision["ID"])
intersection = list(vision["Intersection"])
ip_address = list(vision["Tap/Detection IP"])

log = []
results = []

# Filler value to use to iterate
i = 0

# Determines current date, to append to the file name
today =  pd.to_datetime(date.today())
today = str(today)
today = today.split(" ")
today = str(today[0])

nextstep = "yes"


while i < len(ip_address):
    # Pings the ip_address; if successful, will continue the rest of the program
    #if(s.call(["ping", ip_address[i], "-n", "2"])==0):
        #nextstep = "yes"
    #else:
        #nextstep = "no"

    if nextstep == "yes":
        # Sets the ip address, and what to name the screenshot
        url_format = "http://" + ip_address[i] + "/api/v1/snapshot?timestamp=n&jpeg-quality=100"
        intersection_name = str(id[i]) + " " + intersection[i] + " " + str(today) + " Vision" + ".png"

        # Opens the website
        try:
            time.sleep(5)
            driver.get(url_format)
            driver.save_screenshot(intersection_name)

            result = "Success"

            log.append(([id[i], intersection[i], ip_address[i], result]))
            results = pd.DataFrame(log, columns = ["ID", "Intersection Name", "IP Address", "Result"])

        except:
            result = "Failure"

            log.append(([id[i], intersection[i], ip_address[i], result]))
            results = pd.DataFrame(log, columns = ["ID", "Intersection Name", "IP Address", "Result"])
            
            pass
    i = i + 1

results.to_csv("Vision Screenshot Log " + today + ".csv")

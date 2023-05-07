# Crawler with Single Layer Algorithm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
import logging
import datetime

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sql.sql_func as sql

# set up logging config
logging.basicConfig(level= logging.INFO, format="%(levelname)s (%(asctime)s): %(message)s")
logging.info("start")

# manage command-line args
file = open(sys.argv[1])
urls = file.readlines()

url_start_index = int(sys.argv[2])
url_end_index = int(sys.argv[3])

# set up scan time
scan_time = 20

# set up options for browser
opts = webdriver.FirefoxOptions()
opts.add_argument("--private")
opts.add_argument("--headless")
opts.set_preference('javascript.enabled', False)
opts.set_preference('network.trr.mode', 5)
opts.set_preference("permissions.default.image", 2)
opts.set_preference("http.response.timeout", scan_time)

# initiate browser driver
driver = webdriver.Firefox(options=opts)

# counter for links scanned
globalCounter = 0

def scrape_links(url, stop_time):  
    counter = 1
    logging.info("--" + url.strip('\n') + "--")

    # data structures for BFS
    queue = set()
    
    try:
        # visit first node (layer 0)
        driver.get(url)

        # wait for HTML element with anchor tag to load
        WebDriverWait(driver, scan_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )
    
        # locate HTML anchor tags
        links = driver.find_elements(By.TAG_NAME, "a")

        for link_to_add in links:
            # add links to queue
            href = link_to_add.get_attribute("href")

            if href and href.startswith("http"):
                queue.add(href)
    
    except Exception as e:
        # logging.info(e)
        pass

    # visit first layer
    for i in queue:
        # check time
        try:
            if datetime.datetime.now() >= stop_time:
                # logging.info("Time limit passed")
                logging.info("Scanned: " + str(counter) + " links")
                return
        
            # send request to URL
            driver.get(i)
            # logging.info(f"Scanned: {i}")
            counter += 1
        except Exception as e:
            # logging.info(e)
            pass

    # finish before time limit
    logging.info("Scanned: " + str(counter) + " links")
    globalCounter += counter

# iterate thorugh list of URLs to scrape
for i in range(url_start_index, url_end_index):
    # logging.debug(f"start time for {urls[i]}: {datetime.datetime.now()}")

    link = "http://" + urls[i]
    scrape_links(link, datetime.datetime.now() + datetime.timedelta(seconds=scan_time))

    # logging.debug(f"end time for {urls[i]}: {datetime.datetime.now()}")

    # update all currently not claimed SQLite entries as belonging to the current URL
    try:
        sql.insertOriginalURL(urls[i].strip('\n'))
    except:
        try:
            sql.insertOriginalURL(urls[i].strip('\n'))
        except:
            logging.info("INVALID value: " + urls[i].strip('\n'))

# terminate browser
driver.quit()
logging.info(f"counter: {globalCounter}")
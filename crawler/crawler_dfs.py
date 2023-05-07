# Crawler using DFS Algorithm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import logging
import datetime

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import sql.sql_func as sql

# set up logging config
logging.basicConfig(level=logging.INFO, format="%(levelname)s (%(asctime)s): %(message)s")
logging.info("start")

# manage command-line args
file = open(sys.argv[1])
urls = file.readlines()

url_start_index = int(sys.argv[2])
url_end_index = int(sys.argv[3])

# set up scan time
scan_time = 20
driver_wait_time = 5

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

# set of scraped links
scraped = set()

def scrape_links(url, current_time, stop_time):
    # check timer
    if current_time >= stop_time:
        return
    # check URL if already scraped
    if url in scraped:
        logging.debug(f"Skipping {url}")
        return 
    
    logging.info(f"Scanning: {url}")

    # add scanned url to set
    scraped.add(url)

    # send request to URL
    driver.get(url)

    try:
        # wait for HTML element with anchor tag to load
        WebDriverWait(driver, driver_wait_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )

        # locate HTML anchor tags
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            # obtain links
            href = link.get_attribute("href")
            if href and href.startswith("http"):
                scrape_links(href, datetime.datetime.now(), stop_time)
                
    except Exception as e:
        # log error and continue scraping
        logging.debug(f"Error scraping {url}: {e}")

# iterate thorugh list of URLs to scrape
for i in range(url_start_index, url_end_index):
    logging.debug(f"start time for {urls[i]}: {datetime.datetime.now()}")

    link = "http://" + urls[i]
    scrape_links(link, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(seconds=scan_time))

    logging.debug(f"end time for {urls[i]}: {datetime.datetime.now()}")

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
logging.info(f"counter: {len(scraped)}")

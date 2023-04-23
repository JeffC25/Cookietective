from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import logging
import time

# set up logging config
logging.basicConfig(level=logging.INFO, format="%(levelname)s (%(asctime)s): %(message)s")
logging.info("start")

# manage command-line args
file = open(sys.argv[1])
urls = file.readlines()

url_start_index = int(sys.argv[2])
url_end_index = int(sys.argv[3])

# set up request interval
sleepTime = 1

# # provide path to browser driver
# PATH = "geckodriver"

# set up options for browser
opts = webdriver.FirefoxOptions()
opts.add_argument("--private")
opts.add_argument("--headless")
opts.set_preference('javascript.enabled', False)

# # initiate browser driver
# firefox_service = webdriver.firefox.webdriver.Webdriver(executable_path=PATH)
driver = webdriver.Firefox(options=opts)

# set of scraped links
scraped = set()

def scrape_links(url):

    # check URL if already scraped
    if url in scraped:
        logging.debug("Skipping")
        return 
    
    logging.info(f"Scanning: {url}")

    # add scanned url to set
    scraped.add(url)

    # send request to URL
    driver.get(url)

    try:
        # wait for HTML element with anchor tag to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )

        # locate HTML anchor tags
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            # obtain links
            href = link.get_attribute("href")
            if href and href.startswith("http"):
                scrape_links(href)
                
    except Exception as e:
        # log error and continue scraping
        logging.debug(f"Error scraping {url}: {e}")
        return

    else:
        logging.debug(f"Done scanning: {url}")

# iterate thorugh list of URLs to scrape
for i in range(url_start_index, url_end_index):
    scrape_links("http://" + urls[i])

# terminate browser
driver.quit()
logging.info(f"counter: {len(scraped)}")

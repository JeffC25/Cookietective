from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import logging
import time

# set up options for browser
opts = webdriver.FirefoxOptions()
opts.add_argument("--private")
# opts.set_preference('javascript.enabled', False)
opts.set_preference('network.trr.mode', 5)

# # initiate browser driver
# firefox_service = webdriver.firefox.webdriver.Webdriver(executable_path=PATH)
driver = webdriver.Firefox(options=opts)
driver.get("https://nytimes.com")
time.sleep(10)
driver.quit()

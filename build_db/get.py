import os.path

import requests
import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

five_thirty_eight = "https://projects.fivethirtyeight.com/nba-model/2023/latest_RAPTOR_by_team.csv"
req = requests.get(five_thirty_eight)
table = req.text

data = open("player_stats.csv", "w")
data.write(table)
data.close()
print(os.path.dirname(os.path.realpath(__file__)))
options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", os.path.dirname(os.path.realpath(__file__)))
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

injuries = "https://www.rotowire.com/basketball/injury-report.php"
driver.get(injuries)

time.sleep(3)
button = driver.find_element(By.XPATH, '//button[@class="export-button is-csv"]')
button.click()
time.sleep(3)

driver.close()

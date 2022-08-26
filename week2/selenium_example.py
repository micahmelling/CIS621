"""
Will have to download the Selenium Chrome webdriver: https://chromedriver.chromium.org/downloads
"""

import os
from time import sleep

from selenium import webdriver


def download_file_via_selenium():
    unemployment_data_url = 'https://fred.stlouisfed.org/series/UNRATE'
    driver_path = os.path.join(os.getcwd(), 'chromedriver')
    os.chmod(driver_path, 755)
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get(unemployment_data_url)
    driver.find_element_by_id('download-button').click()
    sleep(5)
    driver.find_element_by_id('download-data-csv').click()
    sleep(5)


if __name__ == "__main__":
    download_file_via_selenium()

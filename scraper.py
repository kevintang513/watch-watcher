import os
import time
import csv
import re

from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

BRANDS = [
    'rolex',
    'omega',
    'tagheuer',
    'seiko',
    'patekphilippe',
    'cartier',
    'iwc',
    'jaegerlecoultre',
    'vacheronconstantin',
    'hamilton',
    'oris',
    'audemarspiguet',
    'tudor',
    'longines',
    'richardmille',
]

# using different user agents in order to resolve invalid session id
options = Options()
ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')

for brand in BRANDS:
    urls = [
        f'https://www.chrono24.com/{brand}/index.htm',
        f'https://www.chrono24.com/{brand}/index-2.htm',
        f'https://www.chrono24.com/{brand}/index-3.htm',
        f'https://www.chrono24.com/{brand}/index-4.htm',
        f'https://www.chrono24.com/{brand}/index-5.htm',
        f'https://www.chrono24.com/{brand}/index-6.htm',
    ]
    data = []

    for url in urls:
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        actions = ActionChains(driver)  # used for mouse-over action
        driver.get(url)

        # accepting data agreement/cookies
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@data-label = 'accept-button']"))
        )
        button.click()

        # scroll to bottom and in order to load images
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        for watch in WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".article-item-container"))):
            try:
                img_div = watch.find_element(
                    By.CSS_SELECTOR, ".article-image-container .content img")
            except NoSuchElementException:
                continue
            try:
                price_text = watch.find_element(
                    By.CSS_SELECTOR, ".article-price strong").text
            except NoSuchElementException:
                continue

            # skip entries without both picture and price
            if (not img_div or not price_text):
                continue
            price = re.sub("[^0-9]", "", price_text)
            # must mouse over images to properly retrieve link
            actions.move_to_element(img_div).perform()
            img_url = img_div.get_attribute('src')
            if (not price or not img_url):
                continue
            # print(img_url)
            data.append([img_url, price])
        driver.close()
    with open(f'data/scraped/{brand}.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(data)
    print(f'{brand} data saved!')

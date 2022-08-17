import dataclasses
from inspect import getmembers
import os
import pickle
import sys
import time
import csv
from datetime import datetime
import re
from glob import glob
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import urllib
import requests

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from rich import print
from scipy import constants

PATH = "/Users/kevintang/chromedriver"

driver = webdriver.Chrome(PATH)

BRANDS = [
    'rolex',
    # 'omega',
    # 'tagheuer',
    # 'seiko',
    # 'patekphilippe',
    # 'cartier',
    # 'iwc',
    # 'jaegerlecoultre',
    # 'vacheronconstantin',
    # 'hamilton',
    # 'oris',
    # 'audemarspiguet',
    # 'tudor',
    # 'longines',
    # 'richardmille',
]

for brand in BRANDS:

    urls = [
        f'https://www.chrono24.com/{brand}/index.htm',
        # f'https://www.chrono24.com/{brand}/index-2.htm',
        # f'https://www.chrono24.com/{brand}/index-3.htm',
        # f'https://www.chrono24.com/{brand}/index-4.htm',
        # f'https://www.chrono24.com/{brand}/index-5.htm',
    ]

    data = []

    for url in urls:
        driver.get(url)
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@data-label = 'accept-button']"))
        )
        button.click()

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        for watch in WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".article-item-container"))):
            try:
                img_div = watch.find_element(By.CSS_SELECTOR, ".article-image-container .content img")
            except NoSuchElementException:
                continue
            try:
                price_text = watch.find_element(By.CSS_SELECTOR, ".article-price strong").text
            except NoSuchElementException:
                continue

            #skip entries without both picture and price
            if (not img_div or not price_text):
                continue
            price = re.sub("[^0-9]", "", price_text)
            img_url = img_div.get_attribute('data-lazy-sweet-spot-master-src')
            if (not price or not img_url):
                continue
            data.append([img_url,price])
                    
    with open(f'data/scraped/{brand}.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(data)




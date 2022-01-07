from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
import configparser
import csv
import sys
import time
import pickle
from bs4 import BeautifulSoup
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pymongo import MongoClient
import pandas as pd
import html
client = MongoClient("mongodb+srv://jeet_scraper:jeet7223@cluster0.xwjgf.mongodb.net/test?retryWrites=true&w=majority")
db  = client.get_database('pt3dstore')
records = db.products


delay = 60
sheet_counter = 1


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
project_name = os.path.dirname(ROOT_DIR)

headless_proxy = "bfd96677d6764ae0a273d342796328f9@proxy.zyte.com:8011"
proxy = {
    "proxyType": "manual",
    "httpProxy": headless_proxy,
    "ftpProxy": headless_proxy,
    "sslProxy": headless_proxy,
    "noProxy": "",
}


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('ignore-certificate-errors')
options.set_capability("proxy", proxy)
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.add_experimental_option("excludeSwitches", ["enable-logging"])
ua = UserAgent()
a = ua.random
user_agent = ua.random
options.add_argument(f'user-agent={user_agent}')
path = project_name+"/chromedriver"
driver = Chrome(executable_path=path,options=options)
browser = driver
product_urls = []
driver.get('https://www.pt3dstore.com/3d-printers')
try:
    products = browser.find_element_by_class_name('product-gallery').find_elements_by_class_name('product-gallery__item--has-button')
except:
    products = []


product_items = []

for prods in products:
    try:
        prod_image = prods.find_element_by_tag_name('img').get_attribute('src')
        prod_url = prods.find_element_by_tag_name('a').get_attribute('href')
        product_items.append([prod_url,prod_image])
    except:
        pass


for pro_items in product_items:
    product_url = pro_items[0]
    main_image  =  pro_items[1]
    driver.get(product_url)

    type =  "product"
    category = "3D Printers"
    try:
        product_title = browser.find_element_by_class_name('product__heading').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        product_title = ""



    try:
        price = browser.find_element_by_css_selector("[itemprop='price']").get_attribute('content')
        price = "€"+price
    except:
        price = ""

    images = []
    try:
        images_list = browser.find_element_by_class_name('product__image-container').find_elements_by_class_name('gallery-item')
        for image_item in images_list:
            try:
                image_url = image_item.get_attribute('href')
                images.append(image_url)
            except:
                pass
    except:
        images = ''

    try:
        description = browser.find_element_by_class_name('product__description').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        description = ""

    try:
        new_product = {
         "_id":product_url,
         "refrence_link":product_url,
         "category":category,
         "type":type,
         "product_title":product_title,
         "description":description,
         "price":price,
         "main_image":main_image,
        }
        if images != "":
            new_product['images'] = images




        records.insert_one(new_product)
        print("Product {} Uploaded Succcessfully".format(sheet_counter))
        sheet_counter = sheet_counter + 1

    except:
        pass
driver.quit()

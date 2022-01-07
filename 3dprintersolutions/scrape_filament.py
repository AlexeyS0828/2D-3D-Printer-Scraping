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
db  = client.get_database('3dprintersolutions')
records = db.filament


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
driver.get('https://www.3dprintersolutions.nl/filament/')
time.sleep(20)
try:
    products = browser.find_element_by_class_name('collection-products-row').find_elements_by_class_name('product-grid')
except:
    products = []

product_urls = []
for prods in products:
    try:
        prod_url = prods.find_element_by_class_name('quickshop').get_attribute('href')
        prod_brand = prods.find_element_by_class_name('brand').get_attribute('innerHTML')
        product_urls.append([prod_url,prod_brand])
    except:
        pass

for prod_items in product_urls:
    product_url = prod_items[0]
    brand = prod_items[1]
    driver.get(product_url)
    type =  "product"
    category = "Filament"
    try:
        product_title = browser.find_element_by_class_name('product-title').find_element_by_tag_name('h1').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        product_title = ""



    try:
        stock_status = browser.find_element_by_class_name('stock').find_element_by_class_name('in-stock')
        stock_status = "In Stock"
    except:
        stock_status = "Out Of Stock"

    try:
        price = browser.find_element_by_class_name('product-price').find_element_by_class_name('price').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        price = ""

    try:
        short_description  = browser.find_element_by_class_name('product-description').get_attribute('innerHTML').split('<a')
        short_description = short_description[0].replace('\n','').replace('  ','')
    except:
        short_description = ""

    try:
        main_image =  browser.find_element_by_id('holder').find_element_by_class_name('swiper-wrapper').find_elements_by_class_name('swiper-slide')[0].find_element_by_tag_name('img').get_attribute('src').replace('/65x75x1/','/')
    except:
        main_image = ""
    images = []
    try:
        images_list = browser.find_element_by_class_name('vertical').find_element_by_class_name('swiper-wrapper').find_elements_by_class_name('swiper-slide')
        for image_item in images_list:
            try:
                image_url = image_item.find_element_by_tag_name('img').get_attribute('src').replace('/65x75x1/','/')
                images.append(image_url)
            except:
                pass
    except:
        images = ''

    try:
        description = browser.find_element_by_id('information').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        description = ""

    related_products = []
    try:
        related_products_list = browser.find_element_by_class_name('products-holder').find_element_by_class_name('swiper-wrapper').find_elements_by_class_name('product-grid')
        for rel_prod in related_products_list:
            prod_link = rel_prod.find_element_by_class_name('quickshop').get_attribute('href')
            related_products.append(prod_link)
    except:
        related_products = ""


    try:
        new_product = {
         "_id":product_url,
         "refrence_link":product_url,
         "category":category,
         "type":type,
         "brand":brand,
         "product_title":product_title,
         "short_description":short_description,
         "description":description,
         "price":price,
         "stock_status":stock_status,
         "main_image":main_image,
        }
        if images != "":
            new_product['images'] = images

        if related_products != "":
            new_product['related_products'] = related_products



        records.insert_one(new_product)
        print("Product {} Uploaded Succcessfully".format(sheet_counter))
        sheet_counter = sheet_counter + 1

    except:
        pass





driver.quit()

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
db  = client.get_database('bcn3d')
records = db.filaments


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

driver.get('https://www.bcn3d.com/bcn3d-filaments/')


try:
    products = browser.find_element_by_class_name('entry-content').find_elements_by_class_name('card-product')
except:
    products = []

product_urls = []
for prod in products:
    prod_url = prod.find_element_by_class_name('woocommerce-loop-product__link').get_attribute('href')
    product_urls.append(prod_url)

for product_url in product_urls:
    driver.get(product_url)
    category = "filaments"
    type =  "product"
    brand = "bcn3d"
    availablity = "In stock"
    try:
        product_title = browser.find_element_by_class_name('product_title').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        product_title = ""

    try:
        product_sub_title = browser.find_element_by_class_name('product_subtitle').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        product_sub_title = ""

    try:
        price = browser.find_element_by_class_name('woocommerce-variation-price').find_element_by_class_name('woocommerce-Price-amount').find_element_by_tag_name('bdi').get_attribute('innerHTML').split('<span')
        price = "€"+price[0]
    except:

        try:
            price  = browser.find_element_by_class_name('price').find_element_by_class_name('woocommerce-Price-amount').find_element_by_tag_name('bdi').get_attribute('innerHTML').split('<span')
            price = "€"+price[0]
        except:
            price = ""
            availablity = "Out Of Stock"

    try:
        main_image = browser.find_element_by_class_name('woocommerce-product-gallery__image').find_element_by_tag_name('img').get_attribute('src')
    except:
        main_image = ""

    try:
        overview = browser.find_element_by_id('filament-overview').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        overview = ""

    try:
        properties_list = browser.find_element_by_id('filament-properties').find_element_by_class_name('aplicactionList').find_elements_by_tag_name('li')
        properties = []
        for pro_items in properties_list:
            pro_item = pro_items.get_attribute('innerHTML').replace('\n','').replace('  ','')
            properties.append(pro_item)
    except:
        properties_list = ""

    try:
        how_it_print = browser.find_element_by_id('filament-how-to-print').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        how_it_print = ""

    gallery = []
    try:
        gallery_items = browser.find_element_by_id('filament-gallery').find_element_by_class_name("uk-slider-items").find_elements_by_tag_name('li')
        for g_item in gallery_items:
            g_list = {}
            try:
                g_title = g_item.find_element_by_class_name('filament-gallery-content').find_element_by_tag_name('h3').get_attribute('innerHTML').replace('\n','').replace('  ','')
                g_content = g_item.find_element_by_class_name('filament-gallery-content').find_element_by_tag_name('span').get_attribute('innerHTML').replace('\n','').replace('  ','')
                g_image = g_item.find_element_by_class_name('filaments-gallery-image').find_element_by_tag_name('img').get_attribute('src')
                g_list['title']  = g_title
                g_list['description']  = g_content
                g_list['image']  = g_image
                gallery.append(g_list)
            except:
                pass
    except:
        gallery = ""
    colors = []
    try:
        colors_list = browser.find_element_by_class_name('variations').find_element_by_id('color').find_elements_by_class_name('attached')
        for color_items in colors_list:
            try:
                color_name = color_items.get_attribute('innerHTML')
                colors.append(color_name)
            except:
                pass

    except:
        colors = ""

    diameters = []
    try:
        diameters_list = browser.find_element_by_class_name('variations').find_element_by_id('diameter').find_elements_by_class_name('attached')
        for d_items in diameters_list:
            try:
                diameter = d_items.get_attribute('innerHTML')
                diameters.append(diameter)
            except:
                pass

    except:
        diameters = ""

    weight = []
    try:
        weight_list = browser.find_element_by_class_name('variations').find_element_by_id('weight').find_elements_by_class_name('attached')
        for weight_items in weight_list:
            try:
                weight_item = weight_items.get_attribute('innerHTML')
                weight.append(weight_item)
            except:
                pass

    except:
        weight = ""






    try:
        new_product = {
         "_id":product_url,
         "refrence_link":product_url,
         "category":category,
         "type":type,
         "brand":brand,
         "product_title":product_title,
         "product_sub_title":product_sub_title,

         'availablity':availablity,
         "main_image":main_image,
        }
        if price != "":
            new_product['price'] = price

        if gallery != "":
            new_product['gallery'] = gallery

        if overview != "":
            new_product['overview'] = overview

        if properties != "":
            new_product['properties'] = properties

        if how_it_print != "":
            new_product['how_it_print'] = how_it_print

        if colors != "":
            new_product['colors'] = colors
        if weight != "":
            new_product['weight'] = weight

        if diameters != "":
            new_product['diameters'] = diameters



        records.insert_one(new_product)
        print("Product {} Uploaded Succcessfully".format(sheet_counter))
        sheet_counter = sheet_counter + 1

    except:
        pass
driver.quit()

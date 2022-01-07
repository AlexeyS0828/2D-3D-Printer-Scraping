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
db  = client.get_database('meer3d')
records = db.consumables


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
driver.get('https://meer3d.nl/product-category/filamenten/?product_count=144')
try:
    products = browser.find_element_by_class_name('products-3').find_elements_by_tag_name('li')
except:
    products = ""
product_urls = []
for prods in products:
    prod_url = prods.find_element_by_tag_name('a').get_attribute('href')
    product_urls.append(prod_url)

for product_url in product_urls:
    driver.get(product_url)
    type =  "product"
    category = "Consumables"
    try:
        product_title = browser.find_element_by_class_name('product_title').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        product_title = ""
    try:
        price = browser.find_element_by_class_name('product-tax-off').find_element_by_class_name('woocommerce-Price-amount').get_attribute('innerHTML').split('</span>')
        price = '€'+price[1].replace('\n','').replace('  ','')
    except:
        price = ""

    try:

        short_description = browser.find_element_by_class_name('woocommerce-product-details__short-description').get_attribute('innerHTML').replace('\n','').replace('  ','')
        try:
            extra_desc = browser.find_element_by_class_name('usps-text-wrapper').get_attribute('innerHTML').replace('\n','').replace('  ','')
            short_description = short_description + extra_desc
        except:
            extra_desc = ""
    except:
        short_description = ""

    try:
        main_image = browser.find_element_by_class_name('avada-product-gallery-thumbs-wrapper').find_element_by_tag_name('ol').find_elements_by_tag_name('li')[0].find_element_by_tag_name('img').get_attribute('src').replace('-100x100','')
    except:
        try:
            main_image = browser.find_element_by_class_name('woocommerce-product-gallery__image').get_attribute('data-thumb').replace('-100x100','')
        except:
            main_image = ""

    images = []
    try:
        images_list = browser.find_element_by_class_name('avada-product-gallery-thumbs-wrapper').find_element_by_tag_name('ol').find_elements_by_tag_name('li')
        for image_item in images_list:
            try:
                image_url = image_item.find_element_by_tag_name('img').get_attribute('src').replace('-100x100','')
                images.append(image_url)
            except:
                pass
    except:
        try:
            images_list = browser.find_element_by_class_name('wcppb-gallery-thumbnails-wrapper').find_elements_by_tag_name('li')
            for image_item in images_list:
                try:
                    image_url = image_item.get_attribute('data-src').replace('-100x100','')
                    images.append(image_url)
                except:
                    pass
        except:
            images = ""

    try:
        description = browser.find_element_by_id('tab-description').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        description = ""

    additional_information = {}
    try:
        add_info_items = browser.find_element_by_id('tab-additional_information').find_element_by_tag_name('table').find_elements_by_tag_name('tr')
        for add_info_item in add_info_items:
            try:
                info_title = add_info_item.find_element_by_tag_name('th').get_attribute('innerHTML').replace('\n','').replace('  ','')
                try:
                    info_value = add_info_item.find_element_by_tag_name('td').find_element_by_tag_name('p').get_attribute('innerHTML').replace('\n','').replace('  ','')
                except:
                    info_value = add_info_item.find_element_by_tag_name('td').get_attribute('innerHTML').replace('\n','').replace('  ','')
                additional_information[info_title] = info_value
            except:
                pass
    except:
        additional_information = ''

    specifications = {}
    try:

        try:
            spec_items = browser.find_element_by_id('tab-specificaties-fabrikant').find_element_by_tag_name('table').find_elements_by_tag_name('tr')
        except:
            spec_items = browser.find_element_by_id('tab-specificaties').find_element_by_tag_name('table').find_elements_by_tag_name('tr')

        for spec_item in spec_items:
            try:
                try:
                    spec_title = spec_item.find_elements_by_tag_name('td')[0].find_element_by_tag_name('strong').get_attribute('innerHTML').replace('\n','').replace('  ','')
                except:
                    spec_title = spec_item.find_elements_by_tag_name('td')[0].get_attribute('innerHTML').replace('\n','').replace('  ','')
                spec_value = spec_item.find_elements_by_tag_name('td')[1].get_attribute('innerHTML').replace('\n','').replace('  ','')
                specifications[spec_title] = spec_value
            except:
                pass
    except:
        specifications = ''

    videos = []
    try:
        videos_items = browser.find_element_by_class_name('elegant-tabs-container').find_elements_by_tag_name('iframe')
        if len(videos_items) == 0:
            videos = ''
        for video_item in videos_items:
            try:
                video_link = video_item.get_attribute('src')
                videos.append(video_link)
            except:
                pass
    except:
        videos = ''

    reviews = []
    try:
        reviews_list = browser.find_element_by_id('reviews').find_element_by_class_name('commentlist').find_elements_by_tag_name('li')
        if len(reviews_list) == 0:
            reviews = ""
        for review_item in reviews_list:
            r_list = {}
            try:
                r_list['reviewed_by'] = review_item.find_element_by_class_name('woocommerce-review__author').get_attribute('innerHTML').replace('\n','').replace('  ','')
                r_list['published_date'] = review_item.find_element_by_class_name('woocommerce-review__published-date').get_attribute('innerHTML').replace('\n','').replace('  ','')
                r_list['description'] = review_item.find_element_by_class_name('description').get_attribute('innerHTML').replace('\n','').replace('  ','')
                r_list['rating'] = review_item.find_element_by_class_name('star-rating').find_element_by_class_name('rating').get_attribute('innerHTML').replace('\n','').replace('  ','')
                reviews.append(r_list)
            except:
                pass
    except:
        reviews = ''

    try:
        new_product = {
         "_id":product_url,
         "refrence_link":product_url,
         "category":category,
         "type":type,
         "product_title":product_title,
         "short_description":short_description,
         'price':price,
         "main_image":main_image,
        }
        if images != "":
            new_product['images'] = images

        if description != "":
            new_product['description'] = description

        if specifications != "":
            new_product['specifications'] = [specifications]

        if additional_information != "":
            new_product['additional_information'] = [additional_information]

        if videos != "":
            new_product['videos'] = videos

        if reviews != "":
            new_product['reviews'] = reviews



        records.insert_one(new_product)
        print("Product {} Uploaded Succcessfully".format(sheet_counter))
        sheet_counter = sheet_counter + 1

    except:
        pass


driver.quit()

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
db  = client.get_database('3dmingda')
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
for i in range(1,10000):
    url = "https://www.3dmingda.com/?m=home&c=Lists&a=index&tid=3&page={}".format(i)
    driver.get(url)
    try:
        products = browser.find_element_by_class_name('ins-product').find_element_by_class_name('content').find_element_by_tag_name('ul').find_elements_by_tag_name('li')
    except:
        products = []
        break
    if len(products) == 0:
        break
    for prods in products:
        prod_url = prods.find_element_by_tag_name('a').get_attribute('href')
        prod_image = prods.find_element_by_tag_name('img').get_attribute('src')
        product_urls.append([prod_url,prod_image])

for product_item in product_urls:
    product_url = product_item[0]
    main_image = product_item[1]
    driver.get(product_url)

    try:
        category = browser.find_element_by_class_name('rt-tit').find_element_by_tag_name('h4').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        category = ""

    try:
        product_title = browser.find_element_by_class_name('product-show').find_element_by_class_name('right').find_element_by_class_name('txt').find_element_by_tag_name('h5').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        product_title = ""

    try:
        short_description = browser.find_element_by_class_name('product-show').find_element_by_class_name('right').find_element_by_class_name('txt').find_element_by_class_name('txt').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        short_description = ""


    images = []
    try:
        images_list = browser.find_element_by_class_name('preview').find_element_by_class_name('swiper-wrapper').find_elements_by_class_name('swiper-slide')
        for image_item in images_list:
            try:
                image_url = image_item.find_element_by_tag_name('img').get_attribute('src')
                images.append(image_url)
            except:
                pass
    except:
        images = ''

    related_products = []
    try:
        rel_prod_list = browser.find_element_by_class_name('recomend-content').find_element_by_class_name('swiper-wrapper').find_elements_by_class_name('swiper-slide')
        for rel_item in rel_prod_list:
            try:
                rel_prod_url = rel_item.find_element_by_tag_name('a').get_attribute('href')
                related_products.append(rel_prod_url)
            except:
                pass
    except:
        related_products = ''

    hot_products = []
    try:
        hot_prod_list = browser.find_element_by_class_name('pro-box').find_element_by_class_name('swiper-wrapper').find_elements_by_class_name('swiper-slide')
        for hot_item in hot_prod_list:
            try:
                hot_prod_url = hot_item.find_element_by_tag_name('a').get_attribute('href')
                hot_products.append(hot_prod_url)
            except:
                pass
    except:
        hot_products = ''

    try:
        description = browser.find_element_by_class_name('content-box').find_element_by_class_name('bd').find_elements_by_tag_name('ul')[0].find_element_by_tag_name('li').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        description = ""

    try:
        parameters_image = browser.find_element_by_class_name('content-box').find_element_by_class_name('bd').find_elements_by_tag_name('ul')[1].find_element_by_tag_name('li').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        parameters_image = ""

    try:
        application = browser.find_element_by_class_name('content-box').find_element_by_class_name('bd').find_elements_by_tag_name('ul')[2].find_element_by_tag_name('li').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        application = ""

    try:
        video_button = browser.find_element_by_class_name('content-box').find_element_by_class_name('hd').find_elements_by_tag_name('ul')[3].find_element_by_tag_name('li')
        driver.execute_script("arguments[0].click();", video_button)
        time.sleep(2)
        video = browser.find_element_by_class_name('content-box').find_element_by_class_name('bd').find_elements_by_tag_name('ul')[3].find_element_by_tag_name('li').find_element_by_tag_name('embed').get_attribute('src')
    except:
        video = ""

    try:
        faq = browser.find_element_by_class_name('content-box').find_element_by_class_name('bd').find_elements_by_tag_name('ul')[4].find_element_by_tag_name('li').get_attribute('innerHTML').replace('\n','').replace('  ','')
    except:
        faq = ""




    type =  "product"
    brand = "Mingda"
    try:
        new_product = {
         "_id":product_url,
         "refrence_link":product_url,
         "category":category,
         "type":type,
         "brand":brand,
         "product_title":product_title,
         "short_description":short_description,
         "main_image":main_image,
        }
        if images != "":
            new_product['images'] = images

        if description != "":
            new_product['description'] = description

        if parameters_image != "":
            new_product['parameters_image'] = parameters_image

        if application != "":
            new_product['application'] = application

        if video != "":
            new_product['video'] = video

        if faq != "":
            new_product['frequently_ask_question'] = faq


        if related_products != "":
            new_product['related_products'] = related_products

        if hot_products != "":
            new_product['hot_products'] = hot_products


        records.insert_one(new_product)
        print("Product {} Uploaded Succcessfully".format(sheet_counter))
        sheet_counter = sheet_counter + 1

    except:
        pass

driver.quit()

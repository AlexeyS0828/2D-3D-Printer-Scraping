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
db  = client.get_database('ultimaker')
records = db.materials


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

driver.get('https://ultimaker.com/materials')
time.sleep(3)
show_all_button = browser.find_element_by_class_name('list-section__footer').find_element_by_tag_name('button')
driver.execute_script("arguments[0].click();",show_all_button)
time.sleep(6)
try:
    products = browser.find_element_by_class_name('list-section__cards').find_elements_by_class_name('list-section__card-wrapper')
except:
    products = []

product_urls = []
for prods in products:
    product_link = prods.find_element_by_class_name('um-card__anchor-overlay').get_attribute('href')
    product_urls.append(product_link)

for product_url in product_urls:
    new_product = {}
    driver.get(product_url)
    time.sleep(7)
    category = "Material"
    type =  "material"
    brand = "ULTIMAKER"
    new_product['_id'] = product_url
    new_product['refrence_link'] = product_url
    new_product['category'] = category
    new_product['type'] = type
    new_product['brand'] = brand
    try:
        product_title = browser.find_element_by_class_name('um-hero__title').get_attribute('innerHTML').replace("\n","").replace("  ","")
        new_product['title'] = product_title
    except:
        product_title = ""


    try:
        description = browser.find_element_by_class_name('um-hero__description').get_attribute('innerHTML').replace("\n","").replace("  ","")
        new_product['description'] = description
    except:
        description = ""

    try:
        images = browser.find_element_by_class_name('um-hero__image-container').find_element_by_tag_name('img').get_attribute('srcset').split(',')
    except:
        images = []



    try:
        main_image = images[0].split('?')
        main_image  = main_image[0]
        new_product['main_image'] = main_image
    except:
        main_image = ""
    try:
        specification_list = browser.find_element_by_class_name('tabbed-content').find_element_by_class_name('tabs__nav').find_elements_by_class_name('tabs__list_item')
        for spec in specification_list:
            tab_button = spec.find_element_by_tag_name('a')
            driver.execute_script("arguments[0].click();",tab_button)
            time.sleep(4)
            spec_category = spec.find_element_by_tag_name('a').get_attribute('innerHTML').replace("\n","").replace("  ","").replace('<!---->','')
            spec_content = browser.find_element_by_css_selector("[aria-label='{}']".format(spec_category)).find_element_by_class_name('content-general__body').get_attribute('innerHTML').replace("\n","").replace("  ","")
            new_product[spec_category] = spec_content
    except:
        pass

    try:
        content = browser.find_element_by_class_name('overview')
        content_title = content.find_element_by_class_name('header-block__title').get_attribute('innerHTML').replace("\n","").replace("  ","")
        section_items = content.find_element_by_class_name('list-section__cards').find_elements_by_class_name('list-section__card-wrapper')
        sec_array = []
        for items in section_items:
            sec_list = {}
            item_title = items.find_element_by_class_name('content-block__content').find_element_by_class_name('content-block__headline').get_attribute('innerHTML').replace("\n","").replace("  ","")
            item_description = items.find_element_by_class_name('content-block__content').find_element_by_class_name('content-block__description').get_attribute('innerHTML').replace("\n","").replace("  ","")
            item_image = items.find_element_by_class_name('content-block__container-image').find_element_by_tag_name('img').get_attribute('data-srcset').split('?')
            item_image = item_image[0]
            sec_list["title"] = item_title
            sec_list["description"] = item_description
            sec_list["image"] = item_image
            sec_array.append(sec_list)
        new_product[content_title] = sec_array
    except:
        pass

    try:
        color_list = browser.find_element_by_class_name('colors__swatches').find_element_by_class_name('colors__list').find_elements_by_class_name('colors__list-item')
        color_counter = 0
        color_array = []
        for color_items in color_list:
            color_list = {}
            color_code = color_items.find_element_by_class_name('color__spec--swatch').get_attribute('style').split(":")
            color_code = color_code[1].replace(";","")
            color_list['color_code'] = color_code
            driver.execute_script("arguments[0].click();",color_items)
            time.sleep(7)
            try:
                color_image = browser.find_element_by_class_name('colors').find_element_by_class_name('flexgrid__cell--sm-8').find_elements_by_tag_name('img')[color_counter].get_attribute('srcset').split(',')
                color_s_image = color_image[0].split("?")
                color_image_final = color_s_image[0]
                color_list['color_image'] = color_image_final
            except:
                pass
            color_counter = color_counter + 1
            color_array.append(color_list)
        new_product["colors"] = color_array
    except:
        pass




    try:
        records.insert_one(new_product)
        print("Product {} Uploaded Succcessfully".format(sheet_counter))
        sheet_counter = sheet_counter + 1
    except:
        pass

driver.quit()

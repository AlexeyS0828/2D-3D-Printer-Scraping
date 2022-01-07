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
db  = client.get_database('xyzprinting')
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
# options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

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

driver.get('https://www.xyzprinting.com/nl-NL/product')
try:
    myElem = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-material-list')))
except TimeoutException:
    print("To slow")

try:
    products = browser.find_element_by_class_name('card-list').find_elements_by_class_name('card-material-list')
except:
    products = []

product_urls = []
for prod in products:
    prod_url = prod.find_element_by_tag_name('a').get_attribute('href')
    product_urls.append(prod_url)


for product_url in product_urls:
    driver.get(product_url)
    try:
        myElem = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'p-item-series')))
    except TimeoutException:
        print("To slow")
    time.sleep(7)

    try:
        product_title = browser.find_element_by_class_name('p-item-series').get_attribute('innerHTML')
        product_title = BeautifulSoup(product_title)
        product_title = product_title.get_text()
    except:
        product_title = ""

    try:
        description = browser.find_element_by_class_name('dmt-control-prodBannerDescription').get_attribute('innerHTML').replace("\n","")
    except:
        description = ""

    try:
        main_image = browser.find_element_by_class_name('single-img-box').find_element_by_tag_name('img').get_attribute('src')
    except:
        main_image = ""

    try:
        videos_link = browser.find_elements_by_class_name('embed-responsive')
        videos = []
        for video in videos_link:
            videos.append(video.find_element_by_class_name('embed-responsive-item').get_attribute('src'))
    except:
        videos = ""

    try:
        features_link  = browser.find_element_by_id('feature').find_elements_by_id('custom-page')[0].find_elements_by_tag_name('section')
        features = []
        for feature in features_link:
            feature = feature.get_attribute('innerHTML').replace("\n","")
            features.append(feature)
    except:
        features = ""

    try:
        related_product_link = browser.find_element_by_id('product-collection').find_elements_by_class_name('btn-fill-color-style')
        related_products = []
        for rel_prod in related_product_link:
            try:
                related_products.append(rel_prod.get_attribute('href'))
            except:
                pass
    except:
        related_products = ""

    try:
        specification_list  = browser.find_element_by_id('spec-container').find_element_by_class_name('spec-content').find_elements_by_class_name('gn-spec')
        specification = []
        spec_list = {}
        for spec in specification_list:
            inner_spec = spec.find_element_by_class_name('list-float').find_elements_by_class_name('gn-spec-item')
            spec_category = spec.find_element_by_class_name('gn-spec-caption').get_attribute('innerHTML')
            list = {}
            for in_spec in inner_spec:

                try:
                    spec_title = in_spec.find_elements_by_tag_name('div')[0].get_attribute('innerHTML').replace("\n","")
                    spec_value = in_spec.find_element_by_class_name('spec-value').get_attribute('innerHTML').replace("\n","")
                    list[spec_title] = spec_value
                except:
                    pass
            spec_list[spec_category] = list
        specification.append(spec_list)

    except:
        specification = ""

    try:
        resources_list = browser.find_element_by_id('resource-container').find_elements_by_class_name('resource-card-container')
        resources = []
        resource_list =  {}
        for resource in resources_list:
            resource_category = resource.find_element_by_class_name('card-title').get_attribute('innerHTML')
            inner_resource = resource.find_element_by_class_name('list-float').find_elements_by_class_name('is-unselectable')
            res_list = []
            for in_res in inner_resource:
                n_list = {}
                try:
                    resource_title = in_res.find_element_by_class_name('item-title').get_attribute('innerHTML')
                    resource_image = in_res.find_element_by_tag_name('img').get_attribute('src')
                    n_list["resource_title"] = resource_title
                    n_list["resource_image"] = resource_image
                    res_list.append(n_list)
                except:
                    pass
            resource_list[resource_category] = res_list
        resources.append(resource_list)

    except:
        resources = ""


    category = "3D PRINTERS"
    type =  "product"
    brand = "XYZPRINTING"

    try:
        new_product = {
         "_id":product_url,
         "refrence_link":product_url,
         "category":category,
         "type":type,
         "brand":brand,
         "name":product_title,
         "description":description,
         "features":features,
         "main_image":main_image
        }
        if videos != "":
            new_product['videos'] = videos

        if specification != "":
            new_product['specifications'] = specification

        if related_products != "":
            new_product['related_products'] = related_products

        if resources != "":
            new_product['resources'] = resources


        records.insert_one(new_product)
        print("Product {} Uploaded Succcessfully".format(sheet_counter))
        sheet_counter = sheet_counter + 1

    except:
        pass




driver.quit()

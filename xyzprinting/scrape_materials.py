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

driver.get('https://www.xyzprinting.com/nl-NL/material')
time.sleep(3)
try:
    myElem = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.ID, "material-list-content")))
except TimeoutException:
    print("To slow")

try:
    materials = browser.find_element_by_id('material-list-content').find_elements_by_class_name('relative')[1].find_elements_by_class_name('card-material-list')
except:
    materials = []

material_data = []
for material in materials:
    prod_url = material.find_element_by_tag_name('a').get_attribute('href')
    material_data.append(prod_url)


for product_url in material_data:
    type =  "material"
    category = "Filament"
    brand = "XYZPRINTING"
    driver.get(product_url)
    time.sleep(7)
    try:
        material_title = browser.find_element_by_id('material-item').find_element_by_class_name('title').get_attribute('innerHTML')
    except:
        material_title = ''

    try:
        description = browser.find_element_by_class_name('dmt-control-materialDescription').get_attribute('innerHTML').replace("\n","")
    except:
        description = ""

    try:
        main_image = browser.find_element_by_id('material-item').find_element_by_class_name('top-img-container').find_element_by_tag_name('img').get_attribute('src')
    except:
        main_image = ''

    try:
        features_link  = browser.find_element_by_class_name('material-content').find_elements_by_class_name('section')
        features = []
        for feature in features_link:
            feature = feature.get_attribute('innerHTML').replace("\n","")
            features.append(feature)
    except:
        features = ""

    try:
        notice_link  = browser.find_element_by_class_name('dmt-control-materialNotice').find_element_by_class_name('list-style-decimal').find_elements_by_tag_name('li')
        important_notice = []
        for notice in notice_link:
            notice = notice.get_attribute('innerHTML').replace("\n","")
            important_notice.append(notice)
    except:
        important_notice = ""

    try:
        compability = browser.find_element_by_id('main-content').find_elements_by_class_name('elem-padding-lg')[0]
        compability_title = compability.find_element_by_class_name("sidebar-caption").get_attribute('innerHTML')
        compatible_model = []
        if compability_title == "Compatibele machines":
            compability_list = compability.find_element_by_class_name("sidebar-list").find_elements_by_class_name('item-desc')
            for compabilities in compability_list:
                list = {}
                try:
                    model_name = compabilities.find_element_by_tag_name('a').get_attribute('innerHTML')
                    model_link = compabilities.find_element_by_tag_name('a').get_attribute('href')
                    list["model_name"] = model_name
                    list["model_link"] = model_link
                    compatible_model.append(list)

                except:
                    pass
        else:
            compatible_model = ""
    except:
        compatible_model = ""

    try:
        try:
            specification = browser.find_element_by_id('main-content').find_elements_by_class_name('elem-padding-lg')[2]
        except:
            specification = browser.find_element_by_id('main-content').find_elements_by_class_name('elem-padding-lg')[1]

        spec_title = specification.find_element_by_class_name("sidebar-caption").get_attribute('innerHTML')
        specifications = []
        s_list = {}
        if spec_title == "Specificaties":
            spec_list = specification.find_element_by_class_name("sidebar-list").find_elements_by_class_name('item-spec')
            for spec in spec_list:

                try:
                    spec_name = spec.find_element_by_class_name('item-name').get_attribute('innerHTML')
                    spec_value = spec.find_element_by_class_name('item-value').get_attribute('innerHTML')
                    s_list[spec_name] = spec_value

                except:
                    pass
            specifications.append(s_list)
        else:
            specifications = ""
    except:
        specifications = ""




    try:
        new_product = {
         "_id":product_url,
         "refrence_link":product_url,
         "category":category,
         "type":type,
         "brand":brand,
         "name":material_title,
         "description":description,
         "features":features,
         "main_image":main_image
        }
        if important_notice != "":
            new_product['important_notices'] = important_notice
        if compatible_model != "":
            new_product['compatible_model'] = compatible_model

        if specifications != "":
            new_product['specifications'] = specifications


        records.insert_one(new_product)
        print("Product {} Uploaded Succcessfully".format(sheet_counter))
        sheet_counter = sheet_counter + 1

    except:
        pass


driver.quit()

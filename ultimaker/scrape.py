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

driver.get('https://ultimaker.com/3d-printers')


try:
    products = browser.find_elements_by_css_selector('.link--large.link.cta-link')
except:
    products = []

product_urls = []
for prod in products:
    prod_url = prod.get_attribute('href')
    if "youtube.com" in prod_url:
        pass
    else:
        product_urls.append(prod_url)



section_2_data = ""
features = ""

for product_url in product_urls:
    driver.get(product_url)
    time.sleep(7)
    category = "PRINTERS"
    type =  "product"
    brand = "ULTIMAKER"
    try:
        product_title = browser.find_element_by_class_name('um-hero__title').get_attribute('innerHTML').replace("\n","").replace("  ","")
    except:
        product_title = ""

    try:
        product_subtitle = browser.find_element_by_class_name('um-hero__subtitle').get_attribute('innerHTML').replace("\n","").replace("  ","")
    except:
        product_subtitle = ""


    try:
        description = browser.find_element_by_class_name('um-hero__description').get_attribute('innerHTML').replace("\n","").replace("  ","")
    except:
        description = ""

    try:
        images = browser.find_element_by_class_name('um-hero__image-container').find_element_by_tag_name('img').get_attribute('srcset').split(',')
    except:
        images = []



    try:
        main_image = images[0].split('?')
        main_image  = main_image[0]
    except:
        main_image = ""

    try:
        videos_button = browser.find_element_by_class_name('overview-ubr').find_element_by_class_name('link--large')
        driver.execute_script("arguments[0].click();",videos_button)
        time.sleep(2)
        video_link = browser.find_element_by_class_name('youtube-video__frame').get_attribute('src')
        close_button = browser.find_element_by_class_name('modal__close')
        driver.execute_script("arguments[0].click();",close_button)
        time.sleep(2)
    except:
        video_link = ""

    try:
        specification_list = browser.find_element_by_class_name('tabbed-table').find_element_by_class_name('tabs__nav').find_elements_by_class_name('tabs__list_item')
        specifications = []
        spec_list = {}
        for spec in specification_list:
            tab_button = spec.find_element_by_tag_name('a')
            driver.execute_script("arguments[0].click();",tab_button)
            time.sleep(2)
            spec_category = spec.find_element_by_tag_name('a').get_attribute('innerHTML').replace("\n","").replace("  ","").replace('<!---->','')
            inner_spec = browser.find_element_by_class_name('tabbed-table').find_element_by_css_selector("[aria-label='{}']".format(spec_category)).find_elements_by_class_name('tab-table-row')
            list = {}
            for in_spec in inner_spec:

                try:
                    try:
                        spec_title = in_spec.find_element_by_class_name('tab-table-row__label--tooltip').find_element_by_class_name('icon-button__label').get_attribute('innerHTML').replace("\n","").replace('  ',"")
                    except:
                        spec_title = in_spec.find_element_by_class_name('tab-table-row__label-text').get_attribute('innerHTML').replace("\n","").replace('  ',"")
                    try:
                        spec_value = in_spec.find_element_by_class_name('tab-table-row__content').find_element_by_class_name('tab-table-row__value').get_attribute('innerHTML').replace("\n","")
                    except:
                        spec_value = in_spec.find_element_by_class_name('tab-table-row__content').get_attribute('innerHTML').replace("\n","")
                    list[spec_title] = spec_value
                except:
                    pass
            spec_list[spec_category] = list
        specifications.append(spec_list)
    except:
        specifications = ""
    how_does_it_work = {}
    try:
        try:
            h_d_i = browser.find_element_by_css_selector("[data-id='How does it work?']")
        except:
            h_d_i = browser.find_element_by_css_selector("[type='ContentHighlight']")

        h_d_i_title = h_d_i.find_element_by_class_name('header-block__title').get_attribute('innerHTML').replace("\n","").replace("  ","")
        h_d_i_sub_title = h_d_i.find_element_by_class_name('header-block__subtitle').get_attribute('innerHTML').replace("\n","").replace("  ","")
        h_d_i_body = h_d_i.find_element_by_class_name('content-highlight__body').get_attribute('innerHTML').replace("\n","").replace("  ","")
        h_d_i_videos_button = h_d_i.find_element_by_class_name('cta-link')
        driver.execute_script("arguments[0].click();",h_d_i_videos_button)
        time.sleep(2)
        h_d_i_videos_link = browser.find_element_by_class_name('youtube-video__frame').get_attribute('src')
        close_button = browser.find_element_by_class_name('modal__close')
        driver.execute_script("arguments[0].click();",close_button)
        time.sleep(2)
        how_does_it_work["title"] = h_d_i_title
        how_does_it_work["sub_title"] = h_d_i_sub_title
        how_does_it_work["body"] = h_d_i_body
        how_does_it_work["videos_link"] = h_d_i_videos_link
    except:
        how_does_it_work = ""

    try:
        section_1_data = {}
        section_1 = browser.find_element_by_class_name('overview-ubr')
        section_title = section_1.find_element_by_class_name('header-block__title').get_attribute('innerHTML').replace("\n","").replace("  ","")
        section_items = browser.find_element_by_class_name('overview-ubr__block-icon-wrapper').find_elements_by_class_name('overview-ubr__block-icon')
        sec_array = []
        for items in section_items:
            items_content = items.find_element_by_class_name('block-icon__headline').get_attribute('innerHTML').replace("\n","").replace("  ","")
            sec_array.append(items_content)
        section_1_data["title"] = section_title
        section_1_data["data"] = sec_array
    except:
        section_1_data = ""

    if sheet_counter == 1:
        try:
            section_2_data = {}
            section_title = "3 easy steps to transform your workflow"
            section_items = browser.find_element_by_class_name('list-section__cards').find_elements_by_class_name('list-section__card-wrapper')
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

            section_2_data["title"] = section_title
            section_2_data["data"] = sec_array

        except:
            section_2_data = ""


    if sheet_counter == 1:
        try:
            feature_data = browser.find_element_by_class_name('table-compare__features').find_elements_by_class_name('table-compare__features-body')
            features = []
            feature_list = {}
            for f_item in feature_data:
                feature_title = f_item.find_element_by_class_name('icon-button__label').get_attribute('innerHTML').replace("\n","").replace("  ","")
                feature_list[feature_title] = "Yes"
            features.append(feature_list)
        except:
            pass
    try:
        new_product = {
         "_id":product_url,
         "refrence_link":product_url,
         "category":category,
         "type":type,
         "brand":brand,
         "title":product_title,
         "sub_title":product_subtitle,
         "description":description,
         "main_image":main_image,
        }
        if specifications != "":
            new_product['specifications'] = specifications

        if features != "":
            new_product['features'] = features

        if video_link != "":
            new_product['video_link'] = video_link
        if how_does_it_work != "":
            new_product['how_does_it_work'] = [how_does_it_work]

        if section_1_data != "":
            new_product['section_1'] = [section_1_data]

        if section_2_data != "":
            new_product['section_2'] = [section_2_data]


        records.insert_one(new_product)
        print("Product {} Uploaded Succcessfully".format(sheet_counter))
        sheet_counter = sheet_counter + 1

    except:
        pass


driver.quit()

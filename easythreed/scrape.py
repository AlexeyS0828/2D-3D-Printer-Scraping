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
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pymongo import MongoClient
import pandas as pd
client = MongoClient("mongodb+srv://jeet_scraper:jeet7223@cluster0.xwjgf.mongodb.net/test?retryWrites=true&w=majority")
db  = client.get_database('easythreed')
records = db.products



sheet_counter = 1


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
project_name = os.path.dirname(ROOT_DIR)

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('ignore-certificate-errors')
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
sheet_counter = 1
def scrapeProduct(product_url,driver,sheet_counter):
    driver.get(product_url)

    try:
        product_title = browser.find_element_by_class_name('product-title-text').get_attribute('innerHTML')
    except:
        product_title = ""

    try:
        selling_price = browser.find_element_by_class_name('product-price-value').get_attribute('innerHTML')
    except:
        selling_price = ""

    try:
        main_image = browser.find_element_by_class_name('magnifier-image').get_attribute('src')
    except:
        main_image = ""

    images_array = []

    try:
        image_1 =  browser.find_element_by_class_name('images-view-list').find_elements_by_class_name('images-view-item')[0].find_element_by_tag_name('img').get_attribute('src').replace('_50x50.jpg_.webp','')
        images_array.append(image_1)
    except:
        image_1 = ""

    try:
        image_2 =  browser.find_element_by_class_name('images-view-list').find_elements_by_class_name('images-view-item')[1].find_element_by_tag_name('img').get_attribute('src').replace('_50x50.jpg_.webp','')
        images_array.append(image_2)

    except:
        image_2 = ""

    try:
        image_3 =  browser.find_element_by_class_name('images-view-list').find_elements_by_class_name('images-view-item')[2].find_element_by_tag_name('img').get_attribute('src').replace('_50x50.jpg_.webp','')
        images_array.append(image_3)
    except:
        image_3 = ""

    try:
        image_4 =  browser.find_element_by_class_name('images-view-list').find_elements_by_class_name('images-view-item')[3].find_element_by_tag_name('img').get_attribute('src').replace('_50x50.jpg_.webp','')
        images_array.append(image_4)
    except:
        image_4 = ""

    try:
        image_5 =  browser.find_element_by_class_name('images-view-list').find_elements_by_class_name('images-view-item')[4].find_element_by_tag_name('img').get_attribute('src').replace('_50x50.jpg_.webp','')
        images_array.append(image_5)
    except:
        image_5 = ""


    try:
        image_6 =  browser.find_element_by_class_name('images-view-list').find_elements_by_class_name('images-view-item')[5].find_element_by_tag_name('img').get_attribute('src').replace('_50x50.jpg_.webp','')
        images_array.append(image_6)
    except:
        image_6 = ""

    try:
        image_7 =  browser.find_element_by_class_name('images-view-list').find_elements_by_class_name('images-view-item')[6].find_element_by_tag_name('img').get_attribute('src').replace('_50x50.jpg_.webp','')
        images_array.append(image_7)
    except:
        image_7 = ""


    try:
        image_8 =  browser.find_element_by_class_name('images-view-list').find_elements_by_class_name('images-view-item')[7].find_element_by_tag_name('img').get_attribute('src').replace('_50x50.jpg_.webp','')
        images_array.append(image_8)
    except:
        image_8 = ""

    try:
        image_9 =  browser.find_element_by_class_name('images-view-list').find_elements_by_class_name('images-view-item')[8].find_element_by_tag_name('img').get_attribute('src').replace('_50x50.jpg_.webp','')
        images_array.append(image_9)
    except:
        image_9 = ""

    try:
        image_10 =  browser.find_element_by_class_name('images-view-list').find_elements_by_class_name('images-view-item')[9].find_element_by_tag_name('img').get_attribute('src').replace('_50x50.jpg_.webp','')
        images_array.append(image_10)
    except:
        image_10 = ""

    try:
        colors_option = browser.find_element_by_class_name('sku-property-list').find_elements_by_tag_name('li')
        colors = []

        for col_option in colors_option:
            colors_list = {}
            try:
                driver.execute_script("arguments[0].click();",col_option)
                time.sleep(3)
                try:
                    color_image = col_option.find_element_by_tag_name('img').get_attribute('src')
                except:
                    color_image = ""
                color_name = col_option.find_element_by_tag_name('img').get_attribute('title')

                thumb_image = browser.find_element_by_class_name('magnifier-image').get_attribute('src')
                colors_list['color_name'] = color_name
                colors_list['color_image'] = color_image
                colors_list['thumb_image'] = thumb_image
                colors.append(colors_list)
            except:
                pass

    except:
        colors = []
    description = ""
    try:
        descriptions = browser.find_element_by_id('product-description').find_elements_by_class_name('detailmodule_html')
        for desc in descriptions:
            description = description + desc.get_attribute('innerHTML')
    except:
        description = ""

    try:
        specification_button = browser.find_element_by_class_name('product-detail-tab').find_element_by_class_name('tab-lists').find_element_by_css_selector("[ae_button_type='tab_specs']")
        driver.execute_script("arguments[0].click();",specification_button)
        time.sleep(3)
        technical_specificatons  = browser.find_element_by_class_name('product-specs-list').find_elements_by_class_name('product-prop')
        specification = []
        specification_list = {}
        for tech_spec in technical_specificatons:

            try:
                spec_title = tech_spec.find_element_by_class_name('property-title').get_attribute('innerHTML').replace(":","").replace("\n","")
                spec_value = tech_spec.find_element_by_class_name('property-desc').get_attribute('innerHTML').replace("  ","").replace("\n","")
                if spec_value != "" and spec_title != "":
                    specification_list[spec_title] = spec_value
            except:
                pass

        specification.append(specification_list)
    except:
        specification = ""

    category = "3D PRINTER"


    print("Now")
    time.sleep(20)
    try:
        new_product = {
         "_id":product_url,
         "refrence_link":product_url,
         "category":category,
         "name":product_title,
         "description":description,
         "main_image":main_image,
         "images":images_array,
         "selling_price":selling_price,
         "specification":specification,
        }
        if len(colors) > 0:
            new_product['colors'] = colors

        records.insert_one(new_product)
        print("Product {} Uploaded Succcessfully".format(sheet_counter))
        sheet_counter = sheet_counter + 1
    except IndexError:
        pass


scrapeProduct("https://www.aliexpress.com/item/32868318832.html?spm=a2g0o.detail.1000023.8.35d430deXbmiWJ",driver,sheet_counter)




driver.quit()

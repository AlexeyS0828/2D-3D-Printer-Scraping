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
db  = client.get_database('tronxy')
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

collection_urls = [["3D PRINTER","https://www.tronxy.com/product-category/3d-printer/"],["PARTS & ACCESSORIES","https://www.tronxy.com/product-category/parts-and-accessories/"],["FILAMENTS","https://www.tronxy.com/product-category/filaments/"]]

for col_url in collection_urls:
    collection_url = col_url[1]
    category_name = col_url[0]
    product_urls = []
    for i in range(1,100):
        page_url = collection_url+"page/{}".format(i)
        driver.get(page_url)
        try:
            products = browser.find_element_by_class_name('products').find_elements_by_tag_name('li')
        except:
            products = []
            break

        for prods in products:
            product_link = prods.find_element_by_class_name('woocommerce-LoopProduct-link').get_attribute('href')
            product_urls.append(product_link)

    for product_url in product_urls:
        driver.get(product_url)
        try:
            product_title = browser.find_element_by_class_name('product_title').get_attribute('innerHTML')
        except:
            product_title = ""

        try:
            short_description = browser.find_element_by_class_name('woocommerce-product-details__short-description').get_attribute('innerHTML').replace('\n',"")
        except:
            short_description  = ""

        try:
            main_image = browser.find_element_by_class_name('flex-control-nav').find_elements_by_tag_name('li')[0].find_element_by_tag_name('img').get_attribute('src').replace('-100x100',"")
        except:
            main_image = ""

        images_array = []

        try:
            image_1 =  browser.find_element_by_class_name('flex-control-nav').find_elements_by_tag_name('li')[0].find_element_by_tag_name('img').get_attribute('src').replace('-100x100',"")
            images_array.append(image_1)
        except:
            image_1 = ""

        try:
            image_2 =  browser.find_element_by_class_name('flex-control-nav').find_elements_by_tag_name('li')[1].find_element_by_tag_name('img').get_attribute('src').replace('-100x100',"")
            images_array.append(image_2)

        except:
            image_2 = ""

        try:
            image_3 =  browser.find_element_by_class_name('flex-control-nav').find_elements_by_tag_name('li')[2].find_element_by_tag_name('img').get_attribute('src').replace('-100x100',"")
            images_array.append(image_3)
        except:
            image_3 = ""

        try:
            image_4 =  browser.find_element_by_class_name('flex-control-nav').find_elements_by_tag_name('li')[3].find_element_by_tag_name('img').get_attribute('src').replace('-100x100',"")
            images_array.append(image_4)
        except:
            image_4 = ""

        try:
            image_5 =  browser.find_element_by_class_name('flex-control-nav').find_elements_by_tag_name('li')[4].find_element_by_tag_name('img').get_attribute('src').replace('-100x100',"")
            images_array.append(image_5)
        except:
            image_5 = ""


        try:
            image_6 =  browser.find_element_by_class_name('flex-control-nav').find_elements_by_tag_name('li')[5].find_element_by_tag_name('img').get_attribute('src').replace('-100x100',"")
            images_array.append(image_6)
        except:
            image_6 = ""

        try:
            image_7 =  browser.find_element_by_class_name('flex-control-nav').find_elements_by_tag_name('li')[6].find_element_by_tag_name('img').get_attribute('src').replace('-100x100',"")
            images_array.append(image_7)
        except:
            image_7 = ""


        try:
            image_8 =  browser.find_element_by_class_name('flex-control-nav').find_elements_by_tag_name('li')[7].find_element_by_tag_name('img').get_attribute('src').replace('-100x100',"")
            images_array.append(image_8)
        except:
            image_8 = ""

        try:
            image_9 =  browser.find_element_by_class_name('flex-control-nav').find_elements_by_tag_name('li')[8].find_element_by_tag_name('img').get_attribute('src').replace('-100x100',"")
            images_array.append(image_9)
        except:
            image_9 = ""

        try:
            image_10 =  browser.find_element_by_class_name('flex-control-nav').find_elements_by_tag_name('li')[9].find_element_by_tag_name('img').get_attribute('src').replace('-100x100',"")
            images_array.append(image_10)
        except:
            image_10 = ""

        try:
            description = browser.find_element_by_id('tab-description').get_attribute('innerHTML').replace('\n',"")
        except:
            description = ""


        try:
            technical_specificatons = browser.find_element_by_id('tab-additional_information').find_element_by_tag_name('table').find_elements_by_tag_name('tr')
            specification = []
            specification_list = {}
            for tech_spec in technical_specificatons:
                try:
                    spec_title = tech_spec.find_element_by_tag_name('th').get_attribute('innerHTML')
                    spec_value = tech_spec.find_element_by_tag_name('td').find_element_by_tag_name('p').get_attribute('innerHTML').replace('=',"")
                    if spec_value != "" and spec_title != "":
                        specification_list[spec_title] = spec_value
                except:
                    pass

            specification.append(specification_list)
        except:
            specification = ""

        try:
            new_product = {
             "_id":product_url,
             "refrence_link":product_url,
             "category":category_name,
             "description":description,
             "short_description":short_description,
             "main_image":main_image,
             "images":images_array,
             "name":product_title,
             "specification":specification,
            }
            records.insert_one(new_product)
            print("Product {} Uploaded Succcessfully".format(sheet_counter))
            sheet_counter = sheet_counter + 1
        except:
            pass

driver.quit()

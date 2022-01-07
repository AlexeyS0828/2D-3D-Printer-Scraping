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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pymongo import MongoClient
import pandas as pd
client = MongoClient("mongodb+srv://jeet_scraper:jeet7223@cluster0.xwjgf.mongodb.net/test?retryWrites=true&w=majority")
db  = client.get_database('kexcelled')
records = db.products


delay = 60
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
driver.get("http://kexcelled.nl/products?category=all-products")

try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'products-container')))
    pass
except TimeoutException:
    print("Loading took too much time!")
product_urls = []
try:
    products = browser.find_element_by_class_name('products-container').find_elements_by_tag_name('a')
    for prods in products:
        try:
            product_urls.append(prods.get_attribute('href'))
        except:
            pass
except:
    pass

for product_url in product_urls:
    driver.get(product_url)
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'view-single-product-page')))
        pass
    except TimeoutException:
        print("Loading took too much time!")

    try:
        product_title = browser.find_element_by_class_name('title-wrapper').find_element_by_tag_name('h1').get_attribute('innerHTML')
    except:
        product_title = ""

    try:
        description = browser.find_element_by_class_name('information').find_elements_by_class_name('description')[0].find_element_by_class_name('ng-star-inserted').get_attribute('innerHTML').replace("\n","")

    except:
        description = ""
    category = "3D PRINTER"
    try:
        technical_specificatons  =browser.find_element_by_class_name('information').find_elements_by_class_name('description')[1].find_element_by_tag_name('ul').find_elements_by_tag_name('li')
        specification = []
        specification_list = {}
        for tech_spec in technical_specificatons:

            try:
                spec_title = tech_spec.find_element_by_tag_name('strong').get_attribute('innerHTML').replace("  ","").replace("\n","")
                spec_value = tech_spec.find_element_by_tag_name('div').get_attribute('innerHTML').replace("  ","").replace("\n","")
                if spec_value != "" and spec_title != "":
                    specification_list[spec_title] = spec_value
            except:
                pass

        specification.append(specification_list)
    except:
        specification = ""

    try:
        downloads_links  =browser.find_element_by_class_name('information').find_elements_by_class_name('description')[2].find_element_by_tag_name('ul').find_elements_by_tag_name('li')
        downloads = []
        download_list = {}
        for download in downloads_links:

            try:
                download_title = download.find_element_by_tag_name('strong').get_attribute('innerHTML')
                download_link = download.find_element_by_tag_name('a').get_attribute('href')
                if download_link != "" and download_title != "":
                    downloads.append(download_link)
            except:
                pass
    except:
        downloads = []

    try:
        main_image = browser.find_element_by_class_name('product-container').find_element_by_class_name('image-comp').find_element_by_tag_name('img').get_attribute('src')
    except:
        main_image = ""

    images_array = []

    try:
        image_1 =  browser.find_element_by_class_name('slider-comp').find_element_by_class_name('container').find_elements_by_class_name('image-comp')[0].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_1)
    except:
        image_1 = ""

    try:
        image_2 =  browser.find_element_by_class_name('slider-comp').find_element_by_class_name('container').find_elements_by_class_name('image-comp')[1].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_2)

    except:
        image_2 = ""

    try:
        image_3 =  browser.find_element_by_class_name('slider-comp').find_element_by_class_name('container').find_elements_by_class_name('image-comp')[2].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_3)
    except:
        image_3 = ""

    try:
        image_4 =  browser.find_element_by_class_name('slider-comp').find_element_by_class_name('container').find_elements_by_class_name('image-comp')[3].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_4)
    except:
        image_4 = ""

    try:
        image_5 =  browser.find_element_by_class_name('slider-comp').find_element_by_class_name('container').find_elements_by_class_name('image-comp')[4].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_5)
    except:
        image_5 = ""


    try:
        image_6 =  browser.find_element_by_class_name('slider-comp').find_element_by_class_name('container').find_elements_by_class_name('image-comp')[5].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_6)
    except:
        image_6 = ""

    try:
        image_7 =  browser.find_element_by_class_name('slider-comp').find_element_by_class_name('container').find_elements_by_class_name('image-comp')[6].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_7)
    except:
        image_7 = ""


    try:
        image_8 =  browser.find_element_by_class_name('slider-comp').find_element_by_class_name('container').find_elements_by_class_name('image-comp')[7].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_8)
    except:
        image_8 = ""

    try:
        image_9 =  browser.find_element_by_class_name('slider-comp').find_element_by_class_name('container').find_elements_by_class_name('image-comp')[8].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_9)
    except:
        image_9 = ""

    try:
        image_10 =  browser.find_element_by_class_name('slider-comp').find_element_by_class_name('container').find_elements_by_class_name('image-comp')[9].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_10)
    except:
        image_10 = ""

    try:
        comparision = browser.find_element_by_class_name('product-attributes-comp').find_elements_by_class_name('align-items-start')
        comparisions = []
        comparision_list = {}
        for comp in comparision:

            try:
                comp_title = comp.find_element_by_tag_name('strong').get_attribute('innerHTML').replace("  ","").replace("\n","")
                comp_value = comp.find_element_by_class_name('grades').find_elements_by_class_name('active')
                comp_value = "{}/5".format(len(comp_value))
                if comp_title != "" and comp_value != "":
                    comparision_list[comp_title] = comp_value
            except:
                pass
        comparisions.append(comparision_list)

    except:
        comparisions = []

    try:
        diameter = browser.find_element_by_class_name('sample-product-comp').find_element_by_class_name('diameter').find_element_by_tag_name('ul').find_elements_by_tag_name('li')
        diameters = []
        for diam in diameter:
            try:
                diam.find_element_by_tag_name('a').get_attribute('innerHTML').replace("  ","").replace("\n","")
            except:
                try:
                    diameter_value = diam.get_attribute('innerHTML').replace("  ","").replace("\n","")
                    diameters.append(diameter_value)
                except:
                    pass
    except:
        diameters = []

    try:
        weight = browser.find_element_by_class_name('sample-product-comp').find_element_by_class_name('weight').find_element_by_tag_name('ul').find_elements_by_tag_name('li')
        weights = []
        for weight_item in weight:
            try:
                weight_item.find_element_by_tag_name('a').get_attribute('innerHTML').replace("  ","").replace("\n","")
            except:
                try:
                    weight_value = weight_item.get_attribute('innerHTML').replace("  ","").replace("\n","")
                    weights.append(weight_value)
                except:
                    pass
    except:
        weights = []

    try:
        colors_option = browser.find_element_by_class_name('sample-product-comp').find_element_by_class_name('color').find_element_by_tag_name('ul').find_elements_by_tag_name('li')
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
                color_name = browser.find_element_by_class_name('sample-product-comp').find_element_by_class_name('color').find_element_by_class_name('helper').get_attribute('innerHTML').split(':')
                if "clear" in color_name[1]:
                    color_name = "Defalut"
                else:
                    color_name = color_name[1].replace("  ","").replace("\n","")

                thumb_image =  browser.find_element_by_class_name('product-container').find_element_by_class_name('image-comp').find_element_by_tag_name('img').get_attribute('src')
                colors_list['color_name'] = color_name
                if color_image != "":
                    colors_list['color_image'] = color_image
                colors_list['thumb_image'] = thumb_image
                colors.append(colors_list)
            except:
                pass

    except:
        colors = []


    try:
        new_product = {
         "_id":product_url,
         "refrence_link":product_url,
         "product_title":product_title,
         "brand":"Kexcelled",
         "category":category,
         "description":description,
         "main_image":main_image,
         "images":images_array,
         "name":product_title,
         "specification":specification,
        }
        if len(comparision) > 0:
            new_product['comparisions'] = comparisions

        if len(downloads) > 0:
            new_product['downloads'] = downloads

        if len(diameters) > 0:
            new_product['diameters'] = diameters

        if len(weights) > 0:
            new_product['weights'] = weights

        if len(colors) > 0:
            new_product['colors'] = colors

        records.insert_one(new_product)
        print("Product {} Uploaded Succcessfully".format(sheet_counter))
        sheet_counter = sheet_counter + 1
    except:
        pass

    time.sleep(2)




driver.quit()

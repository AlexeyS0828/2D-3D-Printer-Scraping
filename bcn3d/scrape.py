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

driver.get('https://www.bcn3d.com/')

try:
    element_to_hover_over = browser.find_element_by_id('menu-item-33').find_element_by_tag_name('a')
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()
    time.sleep(2)
except:
    pass
try:
    products = browser.find_element_by_id('mega-menu1a').find_elements_by_tag_name('li')
except:
    products = []

product_urls = []
for prod in products:
    prod_url = prod.find_element_by_tag_name('a').get_attribute('href')
    product_urls.append(prod_url)

product_urls.append('https://www.bcn3d.com/bcn3d-sigma-d25/')

for product_url in product_urls:
    driver.get(product_url)
    category = "3D Printers"
    type =  "product"
    brand = "bcn3d"
    try:
        product_title = browser.find_element_by_class_name('printer-landing-title').get_attribute('innerHTML').split('<span')
        product_title = product_title[0].replace("\n","").replace("   ","")
        try:
            product_model = browser.find_element_by_class_name('printer-landing-title').find_element_by_tag_name('img').get_attribute('alt')
            product_title = product_title +" "+product_model
        except:
            pass
    except:
        product_title = ""

    try:
        description = browser.find_element_by_class_name('introtext').get_attribute('innerHTML').replace("\n","").replace("   ","")
    except:
        description = ""

    try:
        price = browser.find_element_by_class_name('printer-delivery-time-price').find_elements_by_tag_name('p')[1].find_element_by_tag_name('strong').get_attribute('innerHTML')
    except:
        try:
            price = browser.find_element_by_class_name('printer-delivery-time-price').find_element_by_tag_name('p').find_element_by_tag_name('strong').get_attribute('innerHTML')
        except:
             try:
                 price = browser.find_element_by_class_name('introtext').find_element_by_tag_name('strong').get_attribute('innerHTML')
             except:
                 price= ""

    try:
        delivery_time =  browser.find_element_by_class_name('printer-delivery-time-price').find_elements_by_tag_name('p')[1].find_elements_by_tag_name('span')[1].get_attribute('innerHTML')
    except:
        try:
            delivery_time = browser.find_element_by_class_name('printer-delivery-time-price').find_element_by_tag_name('p').find_element_by_tag_name('span').get_attribute('innerHTML').split('<br>')
            delivery_time = delivery_time[1].replace("\n","").replace("  ","")
        except:
            try:
                delivery_time =  browser.find_element_by_class_name('introtext').find_element_by_tag_name('em').get_attribute('innerHTML').replace("\n","").replace("  ","")
            except:
                delivery_time = ""
    try:
        main_image = browser.find_element_by_class_name('attachment-post-thumbnail').get_attribute('src')
    except:
        try:
            main_image = browser.find_element_by_class_name('printer-thumbnail').find_element_by_tag_name('img').get_attribute('src')
        except:
            main_image = ""

    video_array = []
    try:

        try:
            videos = browser.find_element_by_id('videos').find_elements_by_class_name('uk-button-ghost-white')
        except:

            try:
                videos = browser.find_element_by_id('industrial-power').find_elements_by_class_name('uk-button-ghost-white')
            except:
                videos = browser.find_element_by_class_name('cabinet-feats-vid-webinar').find_elements_by_class_name('uk-button-ghost-white')


        for vid in videos:
            vid_link = vid.get_attribute('href')
            video_array.append(vid_link)
    except:
        videos = ""
    section_material = {}
    try:
        section_material_title = browser.find_element_by_id('materials').find_element_by_class_name('uk-h1').get_attribute('innerHTML').replace("\n","").replace("   ","")
        section_material['title'] = section_material_title
    except:
        section_material = ""
        section_material_title = ""

    try:
        section_material_description = browser.find_element_by_id('materials').find_element_by_class_name('mats-contents-inner').find_element_by_tag_name('p').get_attribute('innerHTML').replace("\n","").replace("   ","")
        section_material['description'] = section_material_description
    except:
        section_material_description = ""
    materials_array = []
    try:
        materials = browser.find_element_by_id('materials').find_element_by_class_name('mats-contents-inner').find_element_by_id('mats-buttons-and-logos').find_element_by_class_name('filament-material-buttons').find_elements_by_tag_name('div')
        for mat_items in materials:
            mat_list = {}
            try:
                material_name = mat_items.find_element_by_tag_name('a').get_attribute('innerHTML')

                material_link = mat_items.find_element_by_tag_name('a').get_attribute('href')
                mat_list['name'] = material_name
                mat_list['link'] = material_link
                materials_array.append(mat_list)
            except:
                pass

        section_material['materials'] = materials_array

    except:
        section_material = ""
    try:
        diemensions = browser.find_element_by_id('dimensions')
    except:
        try:
            diemensions = browser.find_element_by_id('print-size')
        except:
            pass

    images_array = []
    try:
        images = browser.find_element_by_class_name('printer-section-slider').find_element_by_class_name('uk-slideshow-items').find_elements_by_tag_name('li')

        for image in images:
            try:
                image_link  = image.find_element_by_tag_name('img').get_attribute('src')
                images_array.append(image_link)
            except:
                pass
    except:
        images_array = ""

    try:
        model = product_url.split('model=')
        model = model[1].replace('&sc','')
    except:
        model = "w50"
    try:
        length_mm = browser.find_element_by_id('sizes-{}'.format(model)).find_element_by_class_name('mm-contents').find_elements_by_class_name('volume-dimension')[0].get_attribute('innerHTML').replace("\n","").replace("   ","")
    except:
        try:
            length_mm = browser.find_element_by_id('sizes').find_element_by_class_name('mm-contents').find_elements_by_class_name('volume-dimension')[0].get_attribute('innerHTML').replace("\n","").replace("   ","")
        except:
            length_mm = ""

    try:
        width_mm = browser.find_element_by_id('sizes-{}'.format(model)).find_element_by_class_name('mm-contents').find_elements_by_class_name('volume-dimension')[1].get_attribute('innerHTML').replace("\n","").replace("   ","")
    except:
        try:
            width_mm = browser.find_element_by_id('sizes').find_element_by_class_name('mm-contents').find_elements_by_class_name('volume-dimension')[1].get_attribute('innerHTML').replace("\n","").replace("   ","")
        except:
            width_mm = ""
    try:
        height_mm = browser.find_element_by_id('sizes-{}'.format(model)).find_element_by_class_name('mm-contents').find_elements_by_class_name('volume-dimension')[2].get_attribute('innerHTML').replace("\n","").replace("   ","")
    except:
        try:
            height_mm = browser.find_element_by_id('sizes').find_element_by_class_name('mm-contents').find_elements_by_class_name('volume-dimension')[2].get_attribute('innerHTML').replace("\n","").replace("   ","")
        except:
            height_mm = ""


    try:
        length_in = browser.find_element_by_id('sizes-{}'.format(model)).find_element_by_class_name('in-contents').find_elements_by_class_name('volume-dimension')[0].get_attribute('innerHTML').replace("\n","").replace("   ","")
    except:
        try:
            length_in = browser.find_element_by_id('sizes').find_element_by_class_name('in-contents').find_elements_by_class_name('volume-dimension')[0].get_attribute('innerHTML').replace("\n","").replace("   ","")
        except:
            length_in = ""

    try:
        width_in = browser.find_element_by_id('sizes-{}'.format(model)).find_element_by_class_name('in-contents').find_elements_by_class_name('volume-dimension')[1].get_attribute('innerHTML').replace("\n","").replace("   ","")
    except:
        try:
            width_in = browser.find_element_by_id('sizes').find_element_by_class_name('in-contents').find_elements_by_class_name('volume-dimension')[1].get_attribute('innerHTML').replace("\n","").replace("   ","")
        except:
            width_in = ""
    try:
        height_in = browser.find_element_by_id('sizes-{}'.format(model)).find_element_by_class_name('in-contents').find_elements_by_class_name('volume-dimension')[2].get_attribute('innerHTML').replace("\n","").replace("   ","")
    except:
        try:
            height_in = browser.find_element_by_id('sizes').find_element_by_class_name('in-contents').find_elements_by_class_name('volume-dimension')[2].get_attribute('innerHTML').replace("\n","").replace("   ","")
        except:
            height_in = ""

    try:
        cabinet = browser.find_element_by_id('cabinet').get_attribute('innerHTML').replace("\n","").replace("   ","")
    except:
        cabinet = ""

    try:
        perform = browser.find_element_by_id('perform').get_attribute('innerHTML').replace("\n","").replace("   ","")
    except:
        try:
            perform = browser.find_element_by_id('performance').get_attribute('innerHTML').replace("\n","").replace("   ","")
        except:
            perform = ""

    try:
        features = browser.find_element_by_id('printer-features').get_attribute('innerHTML').replace("\n","").replace("   ","")
    except:
        try:
            features = browser.find_element_by_class_name('section-key-features-interactive').get_attribute('innerHTML').replace("\n","").replace("   ","")
        except:
            features = ""

    try:
        renovated_design = browser.find_element_by_id('renovated-design').get_attribute('innerHTML').replace("\n","").replace("   ","")
    except:
        renovated_design = ""
    try:
        new_product = {
         "_id":product_url,
         "refrence_link":product_url,
         "category":category,
         "type":type,
         "brand":brand,
         "name":product_title,
         "price":price,
         "description":description,
         "main_image":main_image,
         "images":images_array,
         "delivery_time":delivery_time,
         "videos":video_array,
        }
        if section_material != "":
            new_product['section_material'] = [section_material]
        if length_mm != "" and width_mm != "" and height_mm != "":
            new_product['Lenght(Millimeters)'] = length_mm
            new_product['Width(Millimeters)'] = width_mm
            new_product["Height(Millimeters)"] = height_mm

        if length_in != "" and width_in != "" and height_in != "":
            new_product['Lenght(Inch)'] = length_in
            new_product['Width(Inch)'] = width_in
            new_product["Height(Inch)"] = height_in

        if cabinet != "":
            new_product['cabinet'] = cabinet

        if perform != "":
            new_product['perform'] = perform

        if features != "":
            new_product['features'] = features

        if renovated_design != "":
            new_product['renovated_design'] = renovated_design

        records.insert_one(new_product)
        print("Product {} Uploaded Succcessfully".format(sheet_counter))
        sheet_counter = sheet_counter + 1

    except:
        pass
driver.quit()

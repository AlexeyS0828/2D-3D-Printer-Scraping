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
db  = client.get_database('geeetech')
records = db.products



sheet_counter = 1
headless_proxy = "bfd96677d6764ae0a273d342796328f9@proxy.zyte.com:8011"
proxy = {
    "proxyType": "manual",
    "httpProxy": headless_proxy,
    "ftpProxy": headless_proxy,
    "sslProxy": headless_proxy,
    "noProxy": "",
}

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
project_name = os.path.dirname(ROOT_DIR)

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('ignore-certificate-errors')
options.set_capability("proxy", proxy)
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.add_experimental_option("excludeSwitches", ["enable-logging"])
ua = UserAgent()
a = ua.random
user_agent = ua.random
options.add_argument(f'user-agent={user_agent}')
path = project_name+"/chromedriver"
driver = Chrome(executable_path=path,options=options)
browser = driver
driver.get("https://www.geeetech.com")

product_urls = []
for i in range(1,9):
    url = "https://www.geeetech.com/products_new.html?page={}&disp_order=6".format(i)
    driver.get(url)
    try:
        products = browser.find_element_by_id('products').find_elements_by_tag_name('li')
    except:
        products = []
        break

    for prods in products:
        prod_url = prods.find_element_by_tag_name('a').get_attribute('href')
        product_urls.append(prod_url)




for product_url in product_urls:
    try:
        driver.get(product_url)
    except:
        continue

    try:
        category = browser.find_element_by_id('navBreadCrumb').find_elements_by_tag_name('a')[1].get_attribute('innerHTML')
    except:
        category = ""

    try:
        sub_category = browser.find_element_by_id('navBreadCrumb').find_elements_by_tag_name('a')[2].get_attribute('innerHTML')
    except:
        sub_category = ""

    try:
        product_title = browser.find_element_by_id('productsTitle').get_attribute('innerHTML')
    except:
        product_title = ""

    try:
        sku = browser.find_element_by_id('allInfo').find_element_by_class_name('productsInfoBoxModeRight').find_elements_by_class_name('blueText')[0].get_attribute('innerHTML')
    except:
        sku = ""

    try:
        stock_qty = browser.find_element_by_id('allInfo').find_element_by_class_name('productsInfoBoxModeRight').find_elements_by_class_name('blueText')[2].get_attribute('innerHTML')
    except:
        stock_qty = ""

    try:
        normal_price = browser.find_element_by_class_name('products_price').find_element_by_class_name('normalprice').get_attribute('innerHTML')
    except:
        normal_price = ""

    try:
        selling_price = browser.find_element_by_class_name('products_price').find_element_by_class_name('productSpecialPrice').get_attribute('innerHTML')
    except:
        selling_price = ""

    try:
        main_image = browser.find_element_by_id('product_flash_show_i').get_attribute('src')
    except:
        main_image = ""

    images_array = []

    try:
        image_1 =  browser.find_element_by_class_name('product_list_li_ul').find_elements_by_class_name('hidd')[0].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_1)
    except:
        image_1 = ""

    try:
        image_2 =  browser.find_element_by_class_name('product_list_li_ul').find_elements_by_class_name('hidd')[1].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_2)

    except:
        image_2 = ""

    try:
        image_3 =  browser.find_element_by_class_name('product_list_li_ul').find_elements_by_class_name('hidd')[2].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_3)
    except:
        image_3 = ""

    try:
        image_4 =  browser.find_element_by_class_name('product_list_li_ul').find_elements_by_class_name('hidd')[3].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_4)
    except:
        image_4 = ""

    try:
        image_5 =  browser.find_element_by_class_name('product_list_li_ul').find_elements_by_class_name('hidd')[4].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_5)
    except:
        image_5 = ""


    try:
        image_6 =  browser.find_element_by_class_name('product_list_li_ul').find_elements_by_class_name('hidd')[5].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_6)
    except:
        image_6 = ""

    try:
        image_7 =  browser.find_element_by_class_name('product_list_li_ul').find_elements_by_class_name('hidd')[6].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_7)
    except:
        image_7 = ""


    try:
        image_8 =  browser.find_element_by_class_name('product_list_li_ul').find_elements_by_class_name('hidd')[7].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_8)
    except:
        image_8 = ""

    try:
        image_9 =  browser.find_element_by_class_name('product_list_li_ul').find_elements_by_class_name('hidd')[8].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_9)
    except:
        image_9 = ""

    try:
        image_10 =  browser.find_element_by_class_name('product_list_li_ul').find_elements_by_class_name('hidd')[9].find_element_by_tag_name('img').get_attribute('src')
        images_array.append(image_10)
    except:
        image_10 = ""

    try:
        description = browser.find_element_by_class_name('productsinfocontent').get_attribute('innerHTML')
    except:
        description = ""

    try:
        specification  = browser.find_element_by_class_name('specification').get_attribute('innerHTML').replace("\n","").replace("  ","")
    except:
        specification = ""


    try:
        package_list  = browser.find_element_by_class_name('packagelist').get_attribute('innerHTML').replace("\n","").replace("  ","")

    except:
        package_list = ""

    try:
        doc_content = browser.find_elements_by_class_name('productInfoBox')
        for docs in doc_content:
            try:
                doc_title = docs.find_element_by_class_name('productsInfoTitle').find_element_by_id('products_document_text').get_attribute('innerHTML').replace("\n","").replace("  ","")
                if doc_title == "Document":
                    document_name = docs.find_element_by_class_name('productsInfoTextContent').find_element_by_tag_name('a').get_attribute('innerHTML').replace("\n","").replace("  ","")
                    document_link = docs.find_element_by_class_name('productsInfoTextContent').find_element_by_tag_name('a').get_attribute('href')
                    document = {
                        "document_name":document_name,
                        "document_link":document_link
                    }
            except:
                pass
    except:
        document = ""

    try:
        related_products_data = browser.find_element_by_class_name('relatives').find_elements_by_class_name('sideBoxContent')
        related_products = []
        for rel_prod in related_products_data:
            related_product_link = rel_prod.find_element_by_class_name('recent_products').get_attribute('href')
            related_products.append(related_product_link)

    except:
        related_products = ""

    try:
        new_product = {
         "_id":product_url,
         "refrence_link":product_url,
         "category":category,
         "sub_category":sub_category,
         "description":description,
         "main_image":main_image,
         "images":images_array,
         "name":product_title,
         "sku":sku,
         "selling_price":selling_price,
         "stock_qty":stock_qty,
        }
        if specification != "":
            new_product["specifications"] = specification
        if document != "":
            new_product["document"] = [document]

        if package_list != "":
            new_product["package_lists"] = package_list
        if normal_price != "":
            new_product["normal_price"] = normal_price
        if related_products != "":
            new_product["related_products"] = related_products

        records.insert_one(new_product)
        print("Product {} Uploaded Succcessfully".format(sheet_counter))
        sheet_counter = sheet_counter + 1
    except:
        pass




driver.quit()

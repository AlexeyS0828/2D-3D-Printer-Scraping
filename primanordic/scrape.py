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
db  = client.get_database('primanordic')
records = db.products




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
driver.get("https://www.primanordic.com/")

time.sleep(3)
login_button = browser.find_element_by_css_selector("[href='#login']")
driver.execute_script("arguments[0].click();", login_button)
time.sleep(2)
email_input = browser.find_element_by_id('email24').send_keys("info@vincitori.nl")
time.sleep(1)
password_input = browser.find_element_by_id('password24').send_keys("print1515")
time.sleep(1)
submit_button = browser.find_element_by_css_selector("[data-testing='submit-login']")
driver.execute_script("arguments[0].click();", submit_button)
time.sleep(3)

categories_urls = ["https://www.primanordic.com/filament-resin"]

sheet_counter = 1
for cats in categories_urls:
    cate_url = cats+"?items=100"
    driver.get(cate_url)
    for i in range(1,100):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    time.sleep(7)
    product_urls = []
    try:
        products = browser.find_element_by_id("js--product-list").find_elements_by_class_name('product-list-item')
        for prods in products:
            prod_url  = prods.find_element_by_tag_name('a').get_attribute('href')
            product_urls.append(prod_url)
    except:
        pass

    for product_url in product_urls:
        driver.get(product_url)
        try:
            category = browser.find_element_by_class_name('product-detail__outer').find_element_by_class_name('breadcrumbs').find_elements_by_tag_name('li')[1].find_element_by_tag_name('a').get_attribute('innerHTML')
        except:
            category = ""

        try:
            sub_category = browser.find_element_by_class_name('product-detail__outer').find_element_by_class_name('breadcrumbs').find_elements_by_tag_name('li')[2].find_element_by_tag_name('a').get_attribute('innerHTML')
        except:
            sub_category = ""

        try:
            child_subcategory = browser.find_element_by_class_name('product-detail__outer').find_element_by_class_name('breadcrumbs').find_elements_by_tag_name('li')[3].find_element_by_tag_name('a').get_attribute('innerHTML')
        except:
            child_subcategory = ""

        try:
            producer = browser.find_element_by_class_name('product-detail__producer').get_attribute('innerHTML').replace("  ","").replace("\n","")
        except:
            producer = ""

        try:
            product_title = browser.find_element_by_class_name('product-detail__title').get_attribute('innerHTML').replace("  ","").replace("\n","")
        except:
            product_title = ""

        try:
            article_1 = browser.find_element_by_class_name('product-detail__attr-info-list').find_elements_by_class_name('product-detail__attr-info-list-item')[0].find_element_by_tag_name('span').get_attribute('innerHTML').replace(" ","").replace("\n","")
        except:
            article_1 = ""

        try:
            article_2 = browser.find_element_by_class_name('product-detail__attr-info-list').find_elements_by_class_name('product-detail__attr-info-list-item')[1].find_element_by_tag_name('span').get_attribute('innerHTML').replace(" ","").replace("\n","")
        except:
            article_2 = ""

        try:
            ean = browser.find_element_by_class_name('product-detail__attr-info-list').find_elements_by_class_name('product-detail__attr-info-list-item')[2].find_element_by_tag_name('span').get_attribute('innerHTML').replace(" ","").replace("\n","")
        except:
            ean = ""

        try:
            mfg_part_no = browser.find_element_by_class_name('product-detail__attr-info-list').find_elements_by_class_name('product-detail__attr-info-list-item')[3].find_element_by_tag_name('span').get_attribute('innerHTML').replace("  ","").replace("\n","")
        except:
            mfg_part_no = ""

        try:
            short_description = browser.find_element_by_class_name("product-detail__short-description").get_attribute('innerHTML')
        except:
            short_description = ""

        try:
            main_image = browser.find_element_by_class_name('single-carousel').find_element_by_class_name('prop-1-1').find_element_by_tag_name('img').get_attribute('src')
        except:
            main_image = ""

        images_array = []

        try:
            image_1 =  browser.find_element_by_id('thumb-carousel').find_elements_by_class_name('prop-1-1')[0].find_element_by_tag_name('picture').get_attribute('data-iesrc').replace('/preview/','/full/')
            images_array.append(image_1)
        except:
            image_1 = ""

        try:
            image_2 =  browser.find_element_by_id('thumb-carousel').find_elements_by_class_name('prop-1-1')[1].find_element_by_tag_name('picture').get_attribute('data-iesrc').replace('/preview/','/full/')
            images_array.append(image_2)

        except:
            image_2 = ""

        try:
            image_3 =  browser.find_element_by_id('thumb-carousel').find_elements_by_class_name('prop-1-1')[2].find_element_by_tag_name('picture').get_attribute('data-iesrc').replace('/preview/','/full/')
            images_array.append(image_3)
        except:
            image_3 = ""

        try:
            image_4 =  browser.find_element_by_id('thumb-carousel').find_elements_by_class_name('prop-1-1')[3].find_element_by_tag_name('picture').get_attribute('data-iesrc').replace('/preview/','/full/')
            images_array.append(image_4)
        except:
            image_4 = ""

        try:
            image_5 =  browser.find_element_by_id('thumb-carousel').find_elements_by_class_name('prop-1-1')[4].find_element_by_tag_name('picture').get_attribute('data-iesrc').replace('/preview/','/full/')
            images_array.append(image_5)
        except:
            image_5 = ""


        try:
            image_6 =  browser.find_element_by_id('thumb-carousel').find_elements_by_class_name('prop-1-1')[5].find_element_by_tag_name('picture').get_attribute('data-iesrc').replace('/preview/','/full/')
            images_array.append(image_6)
        except:
            image_6 = ""

        try:
            image_7 =  browser.find_element_by_id('thumb-carousel').find_elements_by_class_name('prop-1-1')[6].find_element_by_tag_name('picture').get_attribute('data-iesrc').replace('/preview/','/full/')
            images_array.append(image_7)
        except:
            image_7 = ""


        try:
            image_8 =  browser.find_element_by_id('thumb-carousel').find_elements_by_class_name('prop-1-1')[7].find_element_by_tag_name('picture').get_attribute('data-iesrc').replace('/preview/','/full/')
            images_array.append(image_8)
        except:
            image_8 = ""

        try:
            image_9 =  browser.find_element_by_id('thumb-carousel').find_elements_by_class_name('prop-1-1')[8].find_element_by_tag_name('picture').get_attribute('data-iesrc').replace('/preview/','/full/')
            images_array.append(image_9)
        except:
            image_9 = ""

        try:
            image_10 =  browser.find_element_by_id('thumb-carousel').find_elements_by_class_name('prop-1-1')[9].find_element_by_tag_name('picture').get_attribute('data-iesrc').replace('/preview/','/full/')
            images_array.append(image_10)
        except:
            image_10 = ""

        try:
            price = browser.find_element_by_class_name('product-detail-price--sale').find_element_by_tag_name('span').get_attribute('innerHTML').replace('<span class="currency__wrapper">€</span>','').replace(' ','')

        except:
            price = ""

        try:
            stock = browser.find_element_by_class_name('product-detail-stock').get_attribute('innerHTML')
            if "in Stock" in stock:
                stock_status = "In Stock"
            else:
                stock_status = "Out Of Stock"
        except:
            stock_status = ""

        try:
            stock_qty = browser.find_element_by_class_name('product-detail-stock').find_element_by_tag_name('strong').get_attribute('innerHTML').replace("'","").replace(" ","").replace("\n","")
        except:
            stock_qty = ""




        try:
            volume_prices = browser.find_element_by_class_name('graduated-prices-table').find_elements_by_tag_name('tr')
        except:
            volume_prices = ""
        volume_prices_array = []
        volume_prices_list = {}
        try:
            for v_prices in volume_prices:
                v_price_title = v_prices.find_elements_by_tag_name('td')[0].get_attribute('innerHTML')
                v_price_value = v_prices.find_elements_by_tag_name('td')[1].get_attribute('innerHTML').replace('<!---->','').replace("  ","").replace("\n","")
                if v_price_title != "":
                    volume_prices_list[v_price_title] = v_price_value
            volume_prices_array.append(volume_prices_list)
        except:
            pass
        video_array = []
        try:
            video_1 = browser.find_element_by_class_name('product-detail__yt-row').find_elements_by_class_name('embed-responsive-item')[0].get_attribute('src')
            video_array.append(video_1)
        except:
            video_1 = ""

        try:
            video_2 = browser.find_element_by_class_name('product-detail__yt-row').find_elements_by_class_name('embed-responsive-item')[1].get_attribute('src')
            video_array.append(video_2)
        except:
            video_2 = ""

        try:
            product_description  = browser.find_element_by_id('id--accordion__collapse-1').find_element_by_class_name('accordion__body').get_attribute('innerHTML')
        except:
            product_description = ""

        try:
            technical_specificatons  = browser.find_element_by_id('id--accordion__collapse-2').find_element_by_class_name('accordion__body').find_element_by_tag_name('table').find_elements_by_tag_name('tr')
            specification = []
            specification_list = {}
            for tech_spec in technical_specificatons:
                try:
                    tech_spec.find_element_by_tag_name('strong')
                except:
                    spec_title = tech_spec.find_elements_by_tag_name('td')[0].get_attribute('innerHTML')
                    spec_value = tech_spec.find_elements_by_tag_name('td')[1].get_attribute('innerHTML')
                    if spec_value != "" and spec_title != "":
                        specification_list[spec_title] = spec_value

            specification.append(specification_list)
        except:
            try:
                technical_specificatons  = browser.find_element_by_id('id--accordion__collapse-2').find_element_by_class_name('accordion__body').find_element_by_tag_name('ul').find_elements_by_tag_name('li')
                specification = []
                specification_list = {}
                for tech_spec in technical_specificatons:
                    spec_n = tech_spec.get_attribute('innerHTML').split(":")
                    try:
                        spec_title = spec_n[0]
                        spec_value = spec_n[1]
                        if spec_value != "" and spec_title != "":
                            specification_list[spec_title] = spec_value
                    except:
                        pass
                specification.append(specification_list)
            except:
                try:
                    specification = browser.find_element_by_id('id--accordion__collapse-2').find_element_by_class_name('accordion__body').get_attribute('innerHTML')
                except:
                    specification = ""
        try:
            related_products_list = browser.find_element_by_class_name('list-item-carousel').find_element_by_class_name('owl-stage').find_elements_by_class_name('owl-item')
            related_products = []
            for rel_prod in related_products_list:
                rel_prod_url = rel_prod.find_element_by_class_name('product-name').get_attribute('href')
                related_products.append(rel_prod_url)
        except:
            related_products = ""



        try:
            new_product = {
             "_id":product_url,
             "refrence_link":product_url,
             "category":category,
             "sub_category":sub_category,
             "child_subcategory":child_subcategory,
             "desc":product_description,
             "main_image":main_image,
             "images":images_array,
             "name":product_title,
             "price":price,
             "specification":specification,
             "producer":producer,
             "article_no_1":article_1,
             "article_no_2":article_2,
             "ean":ean,
             "manufacturer_part_no":mfg_part_no,
             "stock_status":stock_status,
             "stock_qty":stock_qty,
             "volume_prices":volume_prices_array,
             "videos":video_array,
             "related_products":related_products
            }
            records.insert_one(new_product)
            print("Product {} Uploaded Succcessfully".format(sheet_counter))
            sheet_counter = sheet_counter + 1
        except:
            pass

driver.quit()

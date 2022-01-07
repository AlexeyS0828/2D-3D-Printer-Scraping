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
db  = client.get_database('amazon_nl')
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


def scrapeProduct(driver,sheet_counter):
    try:
        product_title = browser.find_element_by_id('productTitle').get_attribute('innerHTML').replace("\n","")
    except:
        product_title = ""

    try:
        selling_price = browser.find_element_by_id('price_inside_buybox').get_attribute('innerHTML').replace("\n","")
    except:
        selling_price = ""

    try:
        main_image = browser.find_element_by_id('landingImage').get_attribute('src')
    except:
        main_image = ""

    images_array = []
    try:
        stock_status = browser.find_element_by_id('availability').find_element_by_tag_name('span').get_attribute('innerHTML').replace("\n","")
    except:
        stock_status = ""
    try:
        image_1 =  browser.find_element_by_id('altImages').find_elements_by_class_name('imageThumbnail')[0].find_element_by_tag_name('img').get_attribute('src')
        to_replace = image_1.split('.')
        to_replace = to_replace[len(to_replace) - 2]
        image_1 = image_1.replace(to_replace,'')
        image_1 = image_1.replace('..','.')
        images_array.append(image_1)
    except:
        image_1 = ""

    try:
        image_2 =  browser.find_element_by_id('altImages').find_elements_by_class_name('imageThumbnail')[1].find_element_by_tag_name('img').get_attribute('src')
        to_replace = image_2.split('.')
        to_replace = to_replace[len(to_replace) - 2]
        image_2 = image_2.replace(to_replace,'')
        image_2 = image_2.replace('..','.')
        images_array.append(image_2)

    except:
        image_2 = ""

    try:
        image_3 =  browser.find_element_by_id('altImages').find_elements_by_class_name('imageThumbnail')[2].find_element_by_tag_name('img').get_attribute('src')
        to_replace = image_3.split('.')
        to_replace = to_replace[len(to_replace) - 2]
        image_3 = image_3.replace(to_replace,'')
        image_3 = image_3.replace('..','.')
        images_array.append(image_3)
    except:
        image_3 = ""

    try:
        image_4 =  browser.find_element_by_id('altImages').find_elements_by_class_name('imageThumbnail')[3].find_element_by_tag_name('img').get_attribute('src')
        to_replace = image_4.split('.')
        to_replace = to_replace[len(to_replace) - 2]
        image_4 = image_4.replace(to_replace,'')
        image_4 = image_4.replace('..','.')
        images_array.append(image_4)
    except:
        image_4 = ""

    try:
        image_5 =  browser.find_element_by_id('altImages').find_elements_by_class_name('imageThumbnail')[4].find_element_by_tag_name('img').get_attribute('src')
        to_replace = image_5.split('.')
        to_replace = to_replace[len(to_replace) - 2]
        image_5 = image_5.replace(to_replace,'')
        image_5 = image_5.replace('..','.')
        images_array.append(image_5)
    except:
        image_5 = ""


    try:
        image_6 =  browser.find_element_by_id('altImages').find_elements_by_class_name('imageThumbnail')[5].find_element_by_tag_name('img').get_attribute('src')
        to_replace = image_6.split('.')
        to_replace = to_replace[len(to_replace) - 2]
        image_6 = image_6.replace(to_replace,'')
        image_6 = image_6.replace('..','.')
        images_array.append(image_6)
    except:
        image_6 = ""

    try:
        image_7 =  browser.find_element_by_id('altImages').find_elements_by_class_name('imageThumbnail')[6].find_element_by_tag_name('img').get_attribute('src')
        to_replace = image_7.split('.')
        to_replace = to_replace[len(to_replace) - 2]
        image_7 = image_7.replace(to_replace,'')
        image_7 = image_7.replace('..','.')
        images_array.append(image_7)
    except:
        image_7 = ""


    try:
        image_8 =  browser.find_element_by_id('altImages').find_elements_by_class_name('imageThumbnail')[7].find_element_by_tag_name('img').get_attribute('src')
        to_replace = image_8.split('.')
        to_replace = to_replace[len(to_replace) - 2]
        image_8 = image_8.replace(to_replace,'')
        image_8 = image_8.replace('..','.')
        images_array.append(image_8)
    except:
        image_8 = ""

    try:
        image_9 =  browser.find_element_by_id('altImages').find_elements_by_class_name('imageThumbnail')[8].find_element_by_tag_name('img').get_attribute('src')
        to_replace = image_9.split('.')
        to_replace = to_replace[len(to_replace) - 2]
        image_9 = image_9.replace(to_replace,'')
        image_9 = image_9.replace('.','.')
        images_array.append(image_9)
    except:
        image_9 = ""

    try:
        image_10 =  browser.find_element_by_id('altImages').find_elements_by_class_name('imageThumbnail')[9].find_element_by_tag_name('img').get_attribute('src')
        to_replace = image_10.split('.')
        to_replace = to_replace[len(to_replace) - 2]
        image_10 = image_10.replace(to_replace,'')
        image_10 = image_10.replace('..','.')
        images_array.append(image_10)
    except:
        image_10 = ""


    try:
        description = browser.find_element_by_id('aplus').get_attribute('innerHTML').replace('<h2>Product Description</h2>','').replace("\n","")
    except:
        try:
            description = browser.find_element_by_id('productDescription').get_attribute('innerHTML').replace("\n","")
        except:
            description = ""



    try:

        product_features_info = browser.find_element_by_id('feature-bullets').find_element_by_tag_name('ul').find_elements_by_tag_name('li')
        product_features = []
        product_features_list = {}
        for p_features in product_features_info:
            p_features = p_features.find_element_by_tag_name('span').get_attribute('innerHTML').split(':')
            p_features_title  = p_features[0]
            p_features_value = p_features[1]
            if p_features_value != "" and p_features_title != "":
                product_features_list[p_features_title] = p_features_value


        product_features.append(product_features_list)
    except:
        try:
            product_features_info = browser.find_element_by_id('feature-bullets').find_element_by_tag_name('ul').find_elements_by_tag_name('li')
            product_features = []
            for p_features in product_features_info:
                p_features = p_features.find_element_by_tag_name('span').get_attribute('innerHTML').replace("\n","")
                product_features.append(p_features)
        except:
            product_features = ""


    try:

        product_detials_info = browser.find_element_by_id('detailBullets_feature_div').find_element_by_class_name('detail-bullet-list').find_elements_by_tag_name('li')
        product_detials = []
        product_detials_list = {}
        for p_details in product_detials_info:

            try:
                p_detials_title = p_details.find_element_by_class_name('a-list-item').find_elements_by_tag_name('span')[0].get_attribute('innerHTML').replace("\n","").replace('  ','')
                p_detials_value = p_details.find_element_by_class_name('a-list-item').find_elements_by_tag_name('span')[1].get_attribute('innerHTML').replace("\n","").replace('  ','')
                if p_detials_value != "" and p_detials_title != "":
                    product_detials_list[p_detials_title] = p_detials_value
            except:
                pass

        product_detials.append(product_detials_list)
    except:
        product_detials = ""

    try:
        try:
            technical_specificatons  = browser.find_element_by_id('product-specification-table').find_elements_by_tag_name('tr')
        except:
            technical_specificatons  = browser.find_element_by_id('productDetails_techSpec_section_1').find_elements_by_tag_name('tr')
        specification = []
        specification_list = {}
        for tech_spec in technical_specificatons:

            try:
                spec_title = tech_spec.find_element_by_tag_name('th').get_attribute('innerHTML').replace("\n","")
                spec_value = tech_spec.find_element_by_tag_name('td').get_attribute('innerHTML').replace("\n","")
                if spec_value != "" and spec_title != "":
                    specification_list[spec_title] = spec_value
            except:
                pass

        specification.append(specification_list)
    except:
        specification = ""

    try:
        brand = browser.find_element_by_id('bylineInfo').get_attribute('innerHTML').split(':')
        brand  = brand[1]
    except:
        brand = ""

    try:
        old_price = browser.find_element_by_class_name('priceBlockStrikePriceString').get_attribute('innerHTML')
    except:
        old_price = ""

    try:
        color_name  = browser.find_element_by_id('variation_color_name').find_element_by_class_name('selection').get_attribute('innerHTML').replace("\n","").replace("  ","")
    except:
        color_name = ""

    try:
        dispatches_from = browser.find_element_by_id('tabular-buybox-container').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[1].find_element_by_class_name('tabular-buybox-text').get_attribute('innerHTML')
    except:
        dispatches_from = ""

    try:
        sold_by = browser.find_element_by_id('tabular-buybox-container').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_id('sellerProfileTriggerId').get_attribute('innerHTML')
    except:
        try:
            sold_by  = browser.find_element_by_id('tabular-buybox-container').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_class_name('tabular-buybox-text').get_attribute('innerHTML')
        except:
            sold_by = ""

    try:
        rating  = browser.find_element_by_id('averageCustomerReviews').find_element_by_class_name('a-icon-alt').get_attribute('innerHTML')
    except:
        rating  = ""

    try:
        tags_details = browser.find_element_by_id('nav-subnav').find_elements_by_tag_name('a')
        tags = []
        for tag_items in tags_details:
            tag_name = tag_items.find_element_by_tag_name('span').get_attribute('innerHTML').replace("\n","").replace('  ','')
            tags.append(tag_name)

    except:
        tags = ""

    related_products = []

    try:
        view = browser.find_element_by_css_selector("[cel_widget_id='sims-consolidated-2_csm_instrumentation_wrapper']")
        driver.execute_script("arguments[0].scrollIntoView();", view)
        max_page_limit = browser.find_element_by_css_selector("[cel_widget_id='sims-consolidated-2_csm_instrumentation_wrapper']").find_element_by_class_name('a-carousel-page-max').get_attribute('innerHTML')
        for i in range(0,int(max_page_limit)):
            try:
                related_product = browser.find_element_by_css_selector("[cel_widget_id='sims-consolidated-2_csm_instrumentation_wrapper']").find_element_by_tag_name('ol').find_elements_by_tag_name('li')
                for rel_prod in related_product:
                    rel_prod_link = rel_prod.find_element_by_class_name('a-link-normal').get_attribute('href')
                    related_products.append(rel_prod_link)
                next_button =  browser.find_element_by_css_selector("[cel_widget_id='sims-consolidated-2_csm_instrumentation_wrapper']").find_element_by_class_name('a-carousel-goto-nextpage')
                driver.execute_script("arguments[0].click();",next_button)
                time.sleep(3)
            except:
                continue

    except:
        pass
    reviews = []
    try:
        all_review_url = browser.find_element_by_class_name('a-link-emphasis').get_attribute('href')
        driver.get(all_review_url)
        for i in range(1,100000):
            review_url = all_review_url+"&pageNumber={}".format(i)
            driver.get(review_url)
            try:
                myElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'aok-relative')))
            except TimeoutException:
                break
            try:
                review_list = browser.find_element_by_id('cm_cr-review_list').find_elements_by_css_selector("[data-hook='review']")
            except:
                review_list = []
                break
            reviews_list = {}
            for review in review_list:
                try:
                    username = review.find_element_by_class_name('a-profile-name').get_attribute('innerHTML')
                    reviews_list['username'] = username
                except:
                    username = ""
                try:
                    rating = review.find_element_by_css_selector("[data-hook='cmps-review-star-rating']").find_element_by_class_name('a-icon-alt').get_attribute('innerHTML')
                    reviews_list['rating'] = rating
                except:
                    rating = ""
                try:
                    review_title = review.find_element_by_css_selector("[data-hook='review-title']").find_element_by_class_name('cr-original-review-content').get_attribute('innerHTML')
                    reviews_list['review_title'] = review_title
                except:
                    review_title = ""


                try:
                    review_date = review.find_element_by_css_selector("[data-hook='review-date']").get_attribute('innerHTML')
                    reviews_list['review_date'] = review_date
                except:
                    review_title = ""

                try:
                    review_body = review.find_element_by_css_selector("[data-hook='review-body']").find_element_by_class_name('cr-original-review-content').get_attribute('innerHTML').replace("\n","").replace('  ','')
                    reviews_list['review_body'] = review_body
                except:
                    review_body = ""

                reviews.append(reviews_list)
    except:
        pass


    category = "3D Printing & Scanning"


    try:
        new_product = {
         "_id":product_url,
         "refrence_link":product_url,
         "category":category,
         "tags":tags,
         "brand":brand,
         "name":product_title,
         "description":description,
         "product_detials":product_detials,
         "product_features":product_features,
         "stock_status":stock_status,
         "main_image":main_image,
         "images":images_array,
         "deal_price":selling_price,
         "old_price":old_price,
         "dispatches_from":dispatches_from,
         "sold_by":sold_by,
         "rating":rating,
         "specification":specification,
         "related_products":related_products,
         "reviews":reviews,
        }
        if color_name != "":
            new_product["color_name"] = color_name


        records.insert_one(new_product)
        print("Product {} Uploaded Succcessfully".format(sheet_counter))

    except:
        pass

for i in range(1,1000000):
    url = "https://www.amazon.nl/s?k=3d+printer&i=industrial&rh=n%3A16242287031%2Cn%3A16558146031&dc&page={}&language=en".format(i)
    driver.get(url)
    try:
        products  = browser.find_elements_by_class_name('s-no-outline')
    except:
        products = []
    product_urls = []
    for prods in products:
        prod_url = prods.get_attribute('href')
        product_urls.append(prod_url)

    for product_url in product_urls:
        driver.get(product_url)
        scrapeProduct(driver,sheet_counter)
        sheet_counter = sheet_counter + 1





driver.quit()


import requests
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
import os
import sys
import time
import re 

BaseUrl = "https://www.multi-3dprint.nl"
def init_chrome_driver():
    directory = os.path.abspath(os.path.dirname(__file__))
    if os.name == 'nt':
        chrome_driver = '\chromedriver.exe'
    else:
        sys.exit('Program works on windows only.')
    driver = webdriver.Chrome(directory + chrome_driver)
    driver.maximize_window()
    return driver
def get_database():
    from pymongo import MongoClient
    import pymongo
    CONNECTION_STRING = "mongodb+srv://scraping:pwd1026@cluster1.xwjgf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)
    return client['muliti-3d_Alex']
def getUrl(url):

    html = requests.get(url)
    soup  = BeautifulSoup(html.content, "html.parser")
   
    contents = soup.find_all("div", class_ = "hikashop_product_image_subdiv")
    
    links = []
    for content in contents:
        link = content.find('a', href=True)
        link = BaseUrl + link['href']
        links.append(link)
   
    return links
def get_data(individual_link):

    html = requests.get(individual_link)
    soup  = BeautifulSoup(html.content, "html.parser")
    
    product_title = soup.find('span', class_ = "hikashop_product_name_main").text
    try:
        product_price = soup.find('span', class_ = "hikashop_product_price").text
    except:
        product_price = ""

    try:
        product_weight = soup.find('span', class_="hikashop_product_weight_main").text
        # product_weight = re.search(r'[0-9]', 'product_weight_').group()
    except:
        product_weight = ""
    
    image_url = []
    img_src_ = soup.find('div', class_ = "hikashop_small_image_div")
    if img_src_ is not None:
        for image in img_src_.find_all('img'):    
                image_url.append(image['src'])
    try:
        product_description = soup.find('h1', class_ = "product-detail__title").text
    except:
        product_description = ""
    contents = soup.find('div', id = "hikashop_product_description_main")
    
    dbname = get_database()
    collection_name = dbname["get_detail_page"]
    item = {
        "product_title" : product_title,
        "product_description" : product_description,
        "product_weight" : product_weight,
        # "reviews_marks" : len(reviews_marks),
        "image_url" : image_url,
        "product_price": product_price
    }
    collection_name.insert_many([item])
def main():
    urls = [
        
    "https://www.multi-3dprint.nl/webshop/multi-3dprint-aanbiedingen.html",
    "https://www.multi-3dprint.nl/webshop/3d-printers.html"
    ]
    limits = [24, 25]
    
    total_links = []
    i = 0
    for url in urls:
        page =0
        while True:
            links = getUrl(url + "?limitstart={}&limit={}".format(page, limits[i]))
            total_links.extend(links)
            # print(len(links))
            if len(links) < limits[i]:
                break
            page = page + limits[i]
        # links = getUrl(url)    
        i = i + 1
    # print(total_links, len(total_links))
    for individual_link in total_links:
        get_data(individual_link)

if __name__ == '__main__':

    main()

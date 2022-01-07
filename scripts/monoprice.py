import requests
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
import os
import sys
import time
import re 

BaseUrl = "https://www.monoprice.eu"
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
    return client['monoprice_Alex']
def getUrl(url):

    html = requests.get(url)
    soup  = BeautifulSoup(html.content, "html.parser")
   
    contents = soup.find_all("div", class_ = "featured-img product-ratio-75")
    
    links = []
    for content in contents:
        link = content.find('a', href=True)
        link =BaseUrl + link['href']
        links.append(link)
    return links
def get_data(individual_link):

    html = requests.get(individual_link)
    soup  = BeautifulSoup(html.content, "html.parser")
    product_title = soup.find('h1', class_ = "page-heading").text
    product_price = soup.find('span', class_ = "money").text.encode("utf-8")

    sku_collections = soup.find('ul', class_ = "product-sku-collection")
    for li_content in sku_collections.find_all('li'):
        print(li_content.extract)
    rating_inners = soup.find('div', class_ = "rating-inner")
    for reviews_num in rating_inners.find_all('span', class_ = "spr-badge-caption"):
        # print(reviews_num)
        pass
    # spr-icon spr-icon-star-empty
    for reviews_marks in rating_inners.find_all('i', class_ = "spr-icon spr-icon-star"):
        # print(len(reviews_marks))
        pass
    
    image_url = []
    img_src_ = soup.find('div', class_ = "product-image-inner")
    for image in img_src_.find_all('img'):
        image_url.append(image['src'])
    # print(product_title, product_price, image_url, li_content, reviews_num,len(reviews_marks))
    dbname = get_database()
    collection_name = dbname["get_detail_page"]
    item = {
        "product_title" : product_title,
        "li_content" : li_content,
        "reviews_num" : reviews_num,
        "reviews_marks" : len(reviews_marks),
        "image_url" : image_url,
        "product_price": product_price
    }
    collection_name.insert_many([item])
def main():
    urls = [
        "https://www.monoprice.eu/collections/3d-printers",
        "https://www.monoprice.eu/collections/3d-printer-filament",
        "https://www.monoprice.eu/collections/3d-printer-resin",
        "https://www.monoprice.eu/collections/3d-printer-parts-accessories"
    ]
    total_links = []
    for url in urls:
        page = 1
        while True:
            links = getUrl(url + "?page={}".format(page))
            total_links.extend(links)
            # print(len(links))
            if len(links) < 16:
                break
            page = page + 1
        
    # print(total_links, len(total_links))
    for individual_link in total_links:
        get_data(individual_link)

if __name__ == '__main__':

    main()

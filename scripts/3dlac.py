import requests
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
import os
import sys
import time
import re
from ntpath import join

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
    return client['3dlac_Alex']
def get_data(url):

    html = requests.get(url)
    soup  = BeautifulSoup(html.content, "html.parser")
    contents = soup.find("ul", class_ = "products columns-2")
    links = []
    for a in contents.find_all('a',  attrs={'class':'woocommerce-LoopProduct-link'}):
    
        link = a['href']
        links.append(link)
        
    for link in links:
        
        html = requests.get(link)
        soup = BeautifulSoup(html.content, "html.parser")
        try:
            contents = soup.find('div', class_ = "summary entry-summary")
            product_title = contents.find('h1', class_ = "product_title entry-title").text
            product_price_ = contents.find('span', class_ = "woocommerce-Price-amount amount").text.encode("utf-8")
            
            image_url = []
       
            for image in contents.find_all('img'):
            
                image_url.append(image['src'])
                print(image_url)
        except:
            contents = soup.find('div', class_ = "et_pb_row et_pb_row_1")
            product_title = contents.find('div', class_ = "et_pb_module_inner")
            product_price = contents.find('span', class_ = "woocommerce-Price-amount amount").text.encode("utf-8")
          
            image_url = []
       
            for image in contents.find_all('img'):
                image_url.append(image['src'])
                print(image_url)
                product_price = soup.find('span', id= "product_price").text
        
        
        print(product_price, product_title, image_url)
        dbname = get_database()
        collection_name = dbname["get_detail_page"]
        item = {
            "product_title" : product_title,
            "image_url" : image_url,
            "product_price": product_price
        }
        collection_name.insert_many([item])
def main():
    urls = [
        "https://www.3dlac.com/3dlac/3dlac-plus/",
        "https://www.3dlac.com/3dlac/3dlac-product/",
    ]
    for url in urls:
        get_data(url)

if __name__ == '__main__':
    main()

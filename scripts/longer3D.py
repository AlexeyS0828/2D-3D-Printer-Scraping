import requests
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
import os
import sys
import time
import re
from ntpath import join


BASE_URL = "https://www.longer3d.com/"
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
    return client['longer3D_Alex']
def get_data(url):

    html = requests.get(url)
    print(html.status_code)
    soup  = BeautifulSoup(html.content, "html.parser")
    contents = soup.find_all("div", class_ = "main_box")
    links = []
 
    for content in contents:
        link = content.find('a', href=True)
        link =BASE_URL + link['href']
        links.append(link)
        print(link)
    for link in links:
        html = requests.get(link)
        soup = BeautifulSoup(html.content, "html.parser")

        print("-------------------------------------------------------------------------")
        contents = soup.find("ul", class_="a-unordered-list a-vertical a-spacing-mini")
        description = []
        product_description = contents.find('li').text
        description.append(product_description)
     
        product_price = soup.find('span', class_ ='money').text
        image_url = []
        img_src_ = soup.find('ul', class_ = "slides")
        
        for image in img_src_.find_all('img'):
            image_url.append(image['src'])
            
        print(product_price, image_url, description)
        dbname = get_database()
        collection_name = dbname["get_detail_page"]
        item = {
 
            "description" : description,
            "image_url" : image_url,
            "product_price": product_price
        }
        collection_name.insert_many([item])
def main():
    urls = [
        "https://www.longer3d.com/collections/3",
        "https://www.longer3d.com/collections/1",
    ]
    for url in urls:
        get_data(url)

if __name__ == '__main__':
    main()

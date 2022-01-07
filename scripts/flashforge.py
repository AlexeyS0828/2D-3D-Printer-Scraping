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
    return client['flashforge_Alex']
def get_data(url):

    html = requests.get(url)
    soup  = BeautifulSoup(html.content, "html.parser")
    contents = soup.find("ul", class_ = "row products-list")
    links = []
    for a in contents.find_all('a', href=True):
    
        link = a['href']
        links.append(link)
    
    for link in links:
        html = requests.get(link)
        soup = BeautifulSoup(html.content, "html.parser")
        product_title = soup.find('h1', class_ = "product-title").text
        try:
            text_danger = soup.find('span', class_="text-danger ml-1").text
        except:
            text_danger = ""
        
        try:
            reviews_num = soup.find('span', class_="reviews-num").text
        except:
            reviews_num = ""
        sale_description = soup.find('p', class_ = "sale-desc mt-3").text   
        
        product_price = soup.find('span', id= "product_price").text
        
        image_url = []
        img_src_ = soup.find('div', class_ = "image-menu")
        for image in img_src_.find_all('img'):
            # print(image['src'])
            image_url.append(image['src'])
        print(product_price, product_title, image_url, sale_description, reviews_num,text_danger)
        dbname = get_database()
        collection_name = dbname["get_detail_page"]
        item = {
            "product_title" : product_title,
            "text_danger" : text_danger,
            "reviews_num" : reviews_num,
            "sale_description" : sale_description,
            "image_url" : image_url,
            "product_price": product_price
        }
        collection_name.insert_many([item])
def main():
    urls = [
        "https://www.flashforgeshop.com/category/flashforge-3d-printer",
        "https://www.flashforgeshop.com/category/voxelab-3d-printer",
        "https://www.flashforgeshop.com/category/accessories-for-3d-printer",
        "https://www.flashforgeshop.com/category/software-for-3d-printer"
    ]
    for url in urls:
        get_data(url)

if __name__ == '__main__':
    main()

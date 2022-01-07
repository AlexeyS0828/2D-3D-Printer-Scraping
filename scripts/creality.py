import requests
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
import os
import sys
import time
import re 

BaseUrl = "https://creality3d.shop"
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
    return client['creality3D_Alex']
def getUrl(url):

    html = requests.get(url)
    soup  = BeautifulSoup(html.content, "html.parser")
   
    contents = soup.find_all("div", class_ = "grid-view-item product-card")
    
    links = []
    for content in contents:
        link = content.find('a', href=True)
        link = BaseUrl + link['href']
        links.append(link)
    # print(link)
    return links
def get_data(individual_link):

    html = requests.get(individual_link)
    soup  = BeautifulSoup(html.content, "html.parser")
    
    try:
        product_title = soup.find('a', class_ = "gf_product-title").text
    except:
        product_title = ""
    try:
        product_price = soup.find('span', class_ = "gf_product-price money").text.encode("utf-8")
    except:
        product_price = ""
    

    print(individual_link)
    contents = soup.find("ul", class_="cbb-frequently-bought-products")
    
    
    image_url = []
    img_src_ = soup.find('div', class_ = "gf_product-image-thumb")
    if img_src_ is not None:
        for image in img_src_.find_all('img'):    
                image_url.append(image['src'])
    
    
    # contents = soup.find("div", class_ = "gempage-video")
     
    # video_url = contents.select_one("iframe").attrs["src"]
    # print(video_url)
    dbname = get_database()
    collection_name = dbname["get_detail_page"]
    item = {
        "product_title" : product_title,
        # "li_content" : li_content,
        # "reviews_num" : reviews_num,
        # "reviews_marks" : len(reviews_marks),
        "image_url" : image_url,
        "product_price": product_price
    }
    collection_name.insert_many([item])
def main():
    urls = [
        "https://creality3d.shop/collections/3d-printer"
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

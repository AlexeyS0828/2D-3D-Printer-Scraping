import sys
sys.path.append("F:\Works\21-10\2.3DPrinter-Jimmy\my_venv\Lib\site-packages")
import requests
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from pymongo import MongoClient
import os
import time
import re 

from functions import get_database

AppInfo = {
    'APPID': 'bg6023fb7dc88b2',
    'AppSecret': '7fae17036fbf36023dba7973692c27e6'
}

def init_chrome_driver():
    directory = os.path.abspath(os.path.dirname(__file__))
    if os.name == 'nt':
        chrome_driver = '\chromedriver.exe'
    else:
        sys.exit('Program works on windows only.')
    driver = webdriver.Chrome(directory + chrome_driver)
    driver.maximize_window()
    return driver

def get_apitoken():
    url = "https://api.banggood.com/getAccessToken?app_id={}&app_secret={}".format(
        AppInfo["APPID"], AppInfo["AppSecret"]
    )
    response = requests.get(url)

    if response.status_code == 200:
        return response.content
    else:
        return None


def getUrl(url):
    html = requests.get(url)
    soup  = BeautifulSoup(html.content, "html.parser")
    table = soup.find_all("table", id = "sProdList")
    
    # links = []
    # for content in contents:
    #     link = content.find('a', href=True)
    #     link = BaseUrl + link['href']
    #     links.append(link)
    print(table)
    # return links
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
    
    pass

if __name__ == '__main__':
    print("--- starting ---")

    # token = get_apitoken()
    # print(token)

    driver = init_chrome_driver()
    driver.get("https://google.com")
    exit()

    main()

# b'{"code":31010,"msg":"Illegal IP address","lang":"en","ip":"188.43.136.33"}'
"""
https://www.banggood.com/ru/Wholesale-3D-Printer-and-Supplies-c-10741.html


https://www.banggood.com/ru/Wholesale-3D-Printer-and-Supplies-c-10741-0-1-1-60-0_page58.html
https://www.banggood.com/ru/Wholesale-3D-Printer-and-Supplies-c-10741-0-1-1-60-0_page60.html
"""
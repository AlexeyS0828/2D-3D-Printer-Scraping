import sys
sys.path.append("F:\Works\21-10\2_3DPrinters\venv\Lib\site-packages")
import requests
from bs4 import BeautifulSoup
from requests.models import DEFAULT_REDIRECT_LIMIT, Response
from lxml import html
from selenium import webdriver
import os
import time
import re
from ntpath import join
from functions import get_database

def init_chrome_driver():
    directory = os.path.abspath(os.path.dirname(__file__))
    if os.name == 'nt':
        chrome_driver = '\chromedriver.exe'
    else:
        sys.exit('Program works on windows only.')
    driver = webdriver.Chrome(directory + chrome_driver)
    driver.maximize_window()
    return driver


class AutoScraping:

    def get_Url(self, url):
        products = get_contents(url)

    def analysis(self, links):
        contents = []
        for link in links:
            html = requests.get(link)
            content  = BeautifulSoup(html.content, "html.parser")
            contents.append(content)
        print(len(contents))
        soup1 = []
        soup2 = []
        for soup in contents:
            categories_ = soup.findAll("a", class_="category-miniature__image-container")
            soup1.append(categories_)    
            products_ = soup.findAll("section", class_="product-miniature js-product-miniature")
            soup2.append(products_)

def get_contents(url, deep=""):
    links, detail = get_page_contents(url)
    if links is not None:
        if detail["page_type"] == "category":
            print("{} - {} links found in  {}".format(deep, detail['count'], url))
            for link in links:
                contents = get_contents(link, deep=deep+" -> ")
        elif detail["page_type"] == "product":
            print("{} - {} products found in {}".format(deep, detail['qty'], url))
            pages = round(detail['qty'] / detail['sect'] + 0.5)
            for page in range(2, pages + 1):
                link = "{}?page={}".format(url, page)
                contents = get_page_contents(link)
            

def get_page_contents(url):
    html = requests.get(url)
    soup  = BeautifulSoup(html.content, "html.parser")
    
    detail = {
        "page_type":"category"
    }
    categories = soup.findAll(class_="category-miniature__image-container")
    if len(categories) > 0:
        links = []
        for link in categories:
            links.append(link['href'])
        detail["count"] = len(links)
        return links, detail

    products_ = soup.findAll("section", class_="product-miniature js-product-miniature")
    if len(products_) > 0:
        products = []
        for product in products_:
            try:
                href = product.find("a", {"class":"product-miniature__thumbnail"})['href']
                collection_urls.insert_one({"product_url": href})
            except Exception as ex:
                print(ex)
                exit()
        print("---- {} products found {}".format(len(products_), url))
        qty_container = soup.find("div", {"class":"qty-change-container"})
        sect = int(qty_container.find("option", {"selected":"selected"}).text)
        qty = int(soup.find("span", {"class":"js-product-nb"}).text)
        detail = {
            "page_type": "product",
            "count": len(products_),
            "sect": sect,
            "qty": qty
        }
        return products, detail
    return None, None

def get_product_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        content_div = soup.find("div", {"id":"content-wrapper"})
        thumbs = content_div.find("div", {"class":"product-thumbs"})
        imgs = thumbs.find_all("img")
        images = []
        for img in imgs:
            images.append(img['src'].replace("-small_default", "-pdt_540"))
        title = content_div.find("h1", {"class":"product-page__name"}).text
        product_reference_div = content_div.find("div", {"class":"product-page__reference"})
        try:
            sku = product_reference_div.find("span", {"itemprop":"sku"}).text
            ean = product_reference_div.find("span", {"class":"text-badge light"}).text.replace("EAN:", "").strip()
        except:
            sku = ""
            ean = ""
        description = content_div.find("div", {"class":"product-page__short-description"}).text
        current_price = content_div.find("span", {"class":"current-price-display"}).text.replace("\xa0", "")
        price = content_div.find("div", {"class":"product-without-taxes"}).text.replace("\xa0", "")
        
        
        product = {
            "url": url,
            "title": title,
            "sku": sku,
            "EAN": ean,
            "images": images,
            "description": description,
            "price": price,
            "current_price":current_price
        }
        
        collection.insert_one(product)
        print("one product added    {}".format(url))
    except Exception as ex:
        print(ex)
    
    # with open ("botland_product.html", "w") as file:
    #     file.write(str(str(soup).encode("utf-8")))
    # print(product)

if __name__ == '__main__':
    url = "https://botland.com.pl/czesci-zapasowe-drukarki-3d/17976-szyba-do-drukarki-3d-220x220mm-5908233670722.html"

    # get_product_info(url)
    # exit()

    db = get_database()
    collection = db["botland"]
    collection_urls = db.botland_urls

    cursor = collection_urls.find(no_cursor_timeout = True)
    cursor_list = [document for document in cursor]
    print(len(cursor_list))
    for doc in cursor_list:
        if collection.count_documents({'url':doc['product_url']}) > 0:
            continue
        print(doc['product_url'])
        continue

        get_product_info(doc['product_url'])


    exit()
    try: 
        url = "https://botland.com.pl/712-druk-3d-cnc"
       
        wp = AutoScraping()
        # links_ = wp.get_Url(url)  # adding product urls
        # analysis = wp.analysis(links_)
        sys.exit()
    except KeyboardInterrupt:
        sys.exit(1)




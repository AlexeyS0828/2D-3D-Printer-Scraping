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


BaseUrl = "https://nl.farnell.com/"

def init_chrome_driver():
    directory = os.path.abspath(os.path.dirname(__file__))
    if os.name == 'nt':
        chrome_driver = '\chromedriver.exe'
    else:
        sys.exit('Program works on windows only.')
    driver = webdriver.Chrome(directory + chrome_driver)
    return driver


def getUrl(url):
    page = 1
    i = 0
    while True:
        driver = init_chrome_driver()
        current_url = "{}/{}".format(url, page)
        # html = requests.get(current_url)
        driver.get(current_url)
        html = driver.page_source
        soup  = BeautifulSoup(html, "html.parser")
        table = soup.find("table", id = "sProdList")
        products = table.find_all("tr", {"class":"productRow"})
        if len(products) == 0:
            break
        for product in products:
            product_sku = product.find("p", {"class":"sku"}).text.strip()
            if collection.count_documents({"sku":product_sku})>0:
                print("~~~~~~~~~~ {}".format(product_sku))
                continue
            print(product_sku)
            link_td = product.find("td", {"class":"productImage"})
            link = link_td.find("a")
            product_Manufacturer_Part_No = link.text.strip()
            product_url = link['href']
            try:
                product_img = link_td.find("img")['src']
            except:
                product_img = ""
            datasheet_div = product.find("div", {"class":"attachmentIcons"})
            product_data_sheet = datasheet_div.find("a", {"class":"prodDetailsAttachment"})
            if product_data_sheet is not None:
                product_data_sheet = product_data_sheet['href']
            else:
                product_data_sheet = ""
            description_td = product.find("td", {"class":"description"})
            product_description = description_td.find("p", {"class":"productDecription"}).text
            product_manufacturerName = description_td.find("p", {"class":"manufacturerName"}).text

            availability_td = product.find("td", {"class":"availability"})
            availability_span = availability_td.find("span", {"class":"inStockBold"})
            if availability_span is not None:
                product_availability = availability_span.text
            else:
                product_availability = "-"
            listPrice_td = product.find("td", {"class":"enhanceListPrice"})
            product_priceFor = listPrice_td.find("p", {"class":"priceFor"}).text.strip()
            message_div = listPrice_td.find("div", {"class":"specMessage"})
            if message_div is not None:
                product_specMessage = message_div.text.strip()
            else:
                product_specMessage = ""
            qtyColumn_td = product.find("td", {"class":"enhanceQtyColumn"})
            try:
                product_qty = qtyColumn_td.find("span", {"class":"qty"}).text
                product_price = qtyColumn_td.find("span", {"class":"qty_price_range"}).text
            except:
                product_qty = ""
                product_price = ""
            product_extParam_tds = product.find_all("td", {"class":"extParameters"})
            product_extParameters = []
            for item in product_extParam_tds:
                product_extParameters.append(item.text.strip())

            product_item = {
                "sku": product_sku,
                "Manufacturer_Part_No": product_Manufacturer_Part_No,
                "url": product_url,
                "img": product_img,
                "data_sheet": product_data_sheet,
                "description": product_description,
                "manufacturerName": product_manufacturerName,
                "availability": product_availability,
                "priceFor": product_priceFor,
                "specMessage": product_specMessage,
                "qty": product_qty,
                "price": product_price,
                "extParameters": product_extParameters
            }

            collection.insert_one(product_item)
            i = i + 1
            print("{}  --- {} product inserted".format(i, product_sku))
        driver.quit()
        page = page + 1
            
    print("\n\n\n\n  nl.farnell.com  scraping finished:    {} products".format(i))
    # return links

def get_data(individual_link):
    pass

def main():
    url = "https://nl.farnell.com/c/tools-production-supplies/3d-printers-accessories/prl/results"
    getUrl(url=url)

if __name__ == '__main__':

    db = get_database()
    collection = db.farnell
    main()



"""
https://nl.farnell.com/c/tools-production-supplies/3d-printers-accessories/prl/results

"""
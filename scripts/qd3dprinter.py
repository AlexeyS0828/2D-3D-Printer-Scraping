import requests
from bs4 import BeautifulSoup
from lxml import html
from requests.api import get
from selenium import webdriver
import os
import sys
import time
import re 
from functions import get_database

BaseUrl = "http://www.qd3dprinter.com"
def init_chrome_driver():
    directory = os.path.abspath(os.path.dirname(__file__))
    if os.name == 'nt':
        chrome_driver = '\chromedriver.exe'
    else:
        sys.exit('Program works on windows only.')
    driver = webdriver.Chrome(directory + chrome_driver)
    driver.maximize_window()
    return driver


def getUrl(url):
    driver = init_chrome_driver()
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    


def get_data(individual_link):

    pass

def main():
    urls = getUrl(BaseUrl)

    pass

if __name__ == '__main__':
    # db = get_database("qd3dprinter")
    # collection = db.products
    # collection_urls = db.present_product_urls

    main()

import sys
sys.path.append("F:\Works\21-10\2.3DPrinter-Jimmy\venv\Lib\site-packages")
import requests
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from pymongo import MongoClient
import ssl

def get_database(dbname=None):
    MONGO_HOST = "cluster1.xwjgf.mongodb.net"
    MONGO_PORT = "27017"
    MONGO_DB = "scraping_results"
    MONGO_USER = "scraping"
    MONGO_PASS = "pwd1026"
    CONNECTION_STRING = "mongodb+srv://scraping:pwd1026@cluster1.xwjgf.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-1287r0-shard-0&readPreference=primary&ssl=true"
    client = MongoClient(CONNECTION_STRING, ssl_cert_reqs=ssl.CERT_NONE)
    if dbname is None:
        db = client['scraping_results']
    else:
        db = client[dbname]
    print("Connected successfully!!!") 
    return db

def get_database_cluster0(dbname=None):
    MONGO_HOST = "cluster0.xwjgf.mongodb.net"
    MONGO_PORT = "27017"
    MONGO_USER = "scraping"
    MONGO_DB = "scraping_alex"
    MONGO_PASS = "pwd1026"
    CONNECTION_STRING = "mongodb+srv://scraping:pwd1026@cluster0.xwjgf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING, ssl_cert_reqs=ssl.CERT_NONE)
    if dbname is None:
        dbname = MONGO_DB
    db = client[dbname]
    print("Connected successfully!!!") 
    return db

def move_scraping_result(collection_src, collection_dest):
    cursor = collection_src.find(no_cursor_timeout=True)
    cursor_list = [document for document in cursor]
    i = len(cursor_list)
    for doc in cursor_list:
        collection_dest.insert_one(doc)
        print(i)
        i = i - 1
        

import sys
import config
sys.path.append(config.syspath)

import os
import requests
import json
import re
import time, datetime

from functions import get_database, get_database_cluster0, move_scraping_result


class BanggoodAPI:
    def __init__(self):
        self.__appId = 'bg6023fb7dc88b2'
        self.__appSecret = '7fae17036fbf36023dba7973692c27e6'
        self.__domain = 'https://api.banggood.com/'

        self.__accessToken = ''
        self.__tokenCacheFile = ''
        
        self.__task = '' 
        self.__method = 'GET'
        self.__params = []
        self.__lang = 'en'
        self.__currency = 'USD'

        self.__waitingTaskInfo = []
        self.__ch = None
        self.__curlExpireTime = 10

        # self.__ch = curl_init()
        self.__tokenCacheFile = os.path.dirname(__file__) + '/banggoodAPI.token.txt'

    def getCategoryList(self):
        self.__task = 'category/getCategoryList'
        self.__method = 'GET'
        result = self.__doRequest()

        return result

    def getProductInfo(self):
        self.__task = 'product/getProductInfo'
        self.__method = 'GET'
        result = self.__doRequest()

        return result

    def getProductList(self):
        self.__task = 'product/getProductList'
        self.__method = 'GET'
        result = self.__doRequest()

        return result

    def getProductPrice(self):
        self.__task = 'product/GetProductPrice'
        self.__method = 'GET'
        result = self.__doRequest()

        return result

    def getStocks(self):
        self.__task = 'product/getStocks'
        self.__method = 'GET'
        result = self.__doRequest()

        return result
    


    def __requestError(self, error):
        print(error) 
        exit()
	
	#  @desc send api request
	#  @access private
    def __doRequest(self):

        if len(self.__params) == 0:
            self.__requestError('params is empty')

        if self.__task != 'getAccessToken':

            if len(self.__accessToken) == 0:
                self.__getAccessToken()
            
            self.__params['access_token'] = self.__accessToken
            
            if 'lang' not in self.__params:
                self.__params['lang'] = self.__lang

            if 'currency' not in self.__params == 0:
                self.__params['currency'] = self.__currency
         

        apiUrl = self.__domain + self.__task

        if self.__method == 'GET':

            quote = '?'
            for k, v in self.__params.items():
                apiUrl = apiUrl + quote + k + '=' + str(v)
                quote = '&'
        
        response = requests.get(apiUrl)

        if response.status_code != 200:
            self.__requestError("request error")

        result = json.loads(response.content)

        if (result['code'] == 21020):
            self.__accessToken = ''
            result = self.__getAccessToken(False) 

        return result

    def setParams(self, params):
        if len(params) != 0:
            self.__params = params


    def __getAccessToken(self, useCache = True):

        if os.path.isfile(self.__tokenCacheFile) and useCache == True:
            with open(self.__tokenCacheFile, "r") as file:
                accessTokenArr = json.load(file)
            if accessTokenArr['expireTime'] > time.time():
                self.__accessToken = accessTokenArr['accessToken']
        
        # if access_token is empty, send request to get accessToken
        if len(self.__accessToken) == 0:

            if len(self.__task) !=0 :

                self.__waitingTaskInfo = {
                    'task' : self.__task,
                    'method' : self.__method,
                    'params' : self.__params, 
                }


            self.__task = 'getAccessToken'
            self.__params = {'app_id' : self.__appId, 'app_secret' : self.__appSecret}
            self.__method = 'GET'

            result = self.__doRequest()

            if (result['code'] == 0):

                expireTime = time.time() + result['expires_in']
                accessTokenArr = {
                    'accessToken' : result['access_token'],
                    'expireTime' : expireTime,
                    'expireDateTime' : datetime.datetime.fromtimestamp(expireTime).strftime("%a %B %d %H:%M:%S %Z %Y")
                }

                with open(self.__tokenCacheFile, "w") as file:
                    file.write(json.dumps(accessTokenArr))

                self.__accessToken = result['access_token']

                if len(self.__waitingTaskInfo) != 0:

                    self.__task = self.__waitingTaskInfo['task']
                    self.__params = self.__waitingTaskInfo['params']
                    self.__method = self.__waitingTaskInfo['method']

                    self.__waitingTaskInfo = []
                    return self.__doRequest()

            else:

                self.__requestError(result)




def get_allProducts(cat_id):
    page = 1
    while True:
        params = {
            'page': page,
            'cat_id': cat_id
        }
        print("Get products on page {}".format(page))
        bangoodAPI.setParams(params)
        result = bangoodAPI.getProductList()
        if result['code'] != 0:
            error = {
                'error': 'get product list error',
                'params': params,
                'result': result
            }
            print(error)
            exit()
        
        product_list = result['product_list']
        for product in product_list:
            product_dict = {
                'product_id' : product['product_id'],
                'cat_id' : product['cat_id'],
                'product_name' : product['product_name'],
                'img' : product['img'],
                'meta_desc' : product['meta_desc'],
                'add_date' : product['add_date'],
                'modify_date' : product['modify_date'],
            }

            params = {'product_id' : product['product_id']}
            bangoodAPI.setParams(params)
            product_info = bangoodAPI.getProductInfo()
            if product_info['code'] == 0:
                product_dict['currency'] = product_info['currency']
                product_dict['warehouse_list'] = product_info['warehouse_list']
                product_dict['poa_list'] = product_info['poa_list']
                product_dict['description'] = product_info['description']
                collection.insert_one(product_dict)
        
        print("Success register {} products on page {}".format(result['page_size'], page))
        page = page + 1
        if page > result['page_total']:
            break


def get_category_ids():
    cursor = collection.find(no_cursor_timeout=True)
    cursor_list = [document for document in cursor]
    categories = []
    for doc in cursor_list:
        if doc['cat_id'] not in categories:
            categories.append(doc['cat_id'])
    print(categories)
def set_categories():
    cursor = collection.find(no_cursor_timeout=True)
    cursor_list = [document for document in cursor]
    # categories = []
    for doc in cursor_list:
        # if doc['cat_id'] not in categories:
            # categories.append(doc['cat_id'])
        collection.update_one(
            {'product_id':doc['product_id']}, 
            {"$set": {'category':categories[doc['cat_id']]}}
        )
    
def filter_eu_warehouse_products():
    cursor = collection.find(no_cursor_timeout=True)
    cursor_list = [doc for doc in cursor]
    for doc in cursor_list:
        for warehouse in doc['warehouse_list']:
            if warehouse['warehouse'] in eu_warehouse_names:
                collection_eu.insert_one(doc)
                break

def add_products():
    cursor = collection_eu.find(no_cursor_timeout=True)
    cursor_list = [document for document in cursor]
    id_V = collection_products.count_documents({})
    for doc in cursor_list:
        if "®" in doc['product_name']:
            brand = doc['product_name'].split("®")[0]
        else:
            brand = ""
        
        if False:
            price_usd = doc['warehouse_list'][0]['warehouse_price']

            params = {
                "product_id": doc['product_id'],
                "warehouse": doc['warehouse_list'][0]['warehouse'],
                "currency": "EUR"
            }
            bangoodAPI.setParams(params)
            data = bangoodAPI.getProductPrice()
            if data['code'] == 0:
                price_eur = data['productPrice'][0]['price']
            else:
                price_eur = '-'

        new_warehouse_list = []
        for warehouse in doc['warehouse_list']:
            if warehouse['warehouse'] in eu_warehouse_names:
                params = {
                    "product_id": doc['product_id'],
                    "warehouse": warehouse['warehouse'],
                    "currency": "EUR"
                }
                bangoodAPI.setParams(params)
                data = bangoodAPI.getProductPrice()
                if data['code'] == 0:
                    price_eur = data['productPrice'][0]['price']
                else:
                    price_eur = '-'
                new_warehouse = {
                    'warehouse' : warehouse['warehouse'],
                    'price_usd' : warehouse['warehouse_price'],
                    'price_eur' : price_eur
                }
                new_warehouse_list.append(new_warehouse)

        # updating stock data
        params = {
            'product_id' : doc['product_id'],
        }
        bangoodAPI.setParams(params)
        data = bangoodAPI.getStocks()
        if data['code'] == 0:
            for warehouse in data['stocks']:
                if warehouse['warehouse'] in eu_warehouse_names:
                    for index in range(len(new_warehouse_list)):
                        if warehouse['warehouse'] == new_warehouse_list[index]['warehouse']:
                            # poa sum
                            stock_amount = 0
                            for stock in warehouse['stock_list']:
                                stock_amount = stock_amount + stock['stock']
                            new_warehouse_list[index]['stock'] = stock_amount

        product = {
            # 'id_V'              : id_V,
            # 'title'             : '',
            'product_name'      : doc['product_name'],
            'brand'             : brand,
            'productCategory'   : doc['category'],
            'category_id'       : doc['cat_id'],
            'date'              : doc['add_date'],
            # 'link'              : '',
            'product_id'        : doc['product_id'],
            # 'stock_level'     : '',
            # 'proce_time'      : '',
            # 'price_usd'      : price_usd,
            # 'price_eur'      : price_eur,
            'warehouse_list' : new_warehouse_list,
            'img'            : doc['img'],
            'description'    : doc['description'],
            'update_date' : datetime.datetime.now()
        }

        if collection_products.count_documents({'product_id': doc['product_id']}) > 0:
            collection_products.update_one({'product_id': doc['product_id']}, {'$set' : product})
            print("updated  {}".format(doc['product_id']))
        else:
            id_V = id_V + 1
            product['id_V'] = id_V
            collection_products.insert_one(product)
            print("inserted  {}".format(doc['product_id']))
            
        # print(product)
        # exit()


        pass


if __name__ == '__main__':
    
    bangoodAPI = BanggoodAPI()

    eu_warehouse_names = ['CZ', 'ES', 'PL']

    if False:
        params = {
            "product_id": '1890315',
            # "poa_id": '7757',
            "warehouse": 'CN',
            "currency": "EUR"
        }
        bangoodAPI.setParams(params)
        data = bangoodAPI.getProductPrice()
        print(data)
        exit()


    #--------------------------
    db = get_database("scraping_results")
    # collection = db.eu
    # cursor = collection.find(no_cursor_timeout=True)
    # cursor_list = [doc for doc in cursor]
    # i = 0
    # for doc in cursor_list:
    #     i = i + 1
    #     if i > 174:
    #         collection.delete_one({"_id": doc["_id"]})
    #         print(i)
    # exit()
    db0 = get_database_cluster0("scraping_alex")
    # collection_dest = db0['eu']

    c_names = ["botland", "farnell"]
    for c in c_names:
        print(c)
        collection = db[c]
        collection_dest = db0[c]
        move_scraping_result(collection, collection_dest)
    exit()
    #--------------------


    db = get_database()
    collection = db.banggood

    
    cat_id = 10741
    # for page in range(1,9):
    #     params = {"page":page}
    #     bangoodAPI.setParams(params=params)

    #     categories = bangoodAPI.getCategoryList()

    #     with open("categories.json", "a") as f:
    #         f.write(json.dumps(categories))
    #         f.write("\n\n\n")


    categories = {
        10741 : "3D Printer & Supplies",
        10742 : "3D Printer Accessories",
        10808 : "3D Printer",
        10745 : "3D Printer Filament",
        10743 : "3D Printer Module Board",
        10747 : "3D Printer Pen"
    }
    # get_category_ids()                    #   ---01---

    # get_allProducts(cat_id=cat_id)        #   ---02---

    # set_categories() #add category names  #   ---03---
    
    collection_eu = db.eu  #  ['CZ', 'ES', 'PL']
    # filter_eu_warehouse_products()        #   ---04---

    db = get_database("banggood")
    collection_products = db.products
    # collection_products = db.banggood_products
    add_products()                          #   ---05---

    print('completed')


    # Product ID V
    # Title
    # Brand
     # Productcategory
     # Date
    # Link
     # Product ID S
    # Stock (level)
    # Proce. time (wd)
    # Price in USD
    # Price in EUR
    # MSRP

    # Incoming
    # Re-stock date
    # EAN Code
    # Status NL
    # Status BE
    # Remark
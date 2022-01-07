from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pymongo import MongoClient
import pandas as pd
SERVICE_ACCOUNT_FILE = "../service.json"

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
worksheet = client.open_by_key('1g7blgcQjpEzNLkMLT0NNL5qQJrs2MFUtoti_H-l5J18').sheet1


client = MongoClient("mongodb+srv://jeet_scraper:jeet7223@cluster0.xwjgf.mongodb.net/test?retryWrites=true&w=majority")
db  = client.get_database('kexcelled')
records = db.products
counter = 1
data = records.find()
for item in data:
    ref_link  = item['refrence_link']
    category = item['category']
    product_title = item['product_title']
    brand = item['brand']
    date = datetime.today().strftime('%d-%m-%Y')
    row = [counter,product_title,brand,category,date,ref_link,"","","","","","MSRP"]
    worksheet.append_row(row)
    print("Product {} Uppload To Sourcing Sheet Succcessfully".format(counter))
    counter = counter +1
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

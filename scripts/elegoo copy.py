import requests
from bs4 import BeautifulSoup

def get_database():
    from pymongo import MongoClient
    import pymongo
    CONNECTION_STRING = "mongodb+srv://scraping:pwd1026@cluster1.xwjgf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)
    return client['scraping_db']
def get_page(url, proxies, headers,verify):
    
    response = requests.get(url, proxies=proxies, headers=headers, verify=False)
    if not response.ok:
        print('server responded:', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
    return soup
grid_products=[]
product_titles=[]
product_prices=[]
href_list=[]
def get_detail_page(soup):
    Mars_printers = soup.find_all('div',class_="grid-product__content",id=False)
    for Mars_printer in Mars_printers:
        grid_product_img_src = ""
        if Mars_printer.find('div', attrs={'class':'grid-product__tag--new'}):
            grid_product_div = Mars_printer.find('div', attrs={'class':'grid-product__tag--new'})
            grid_product_img_src ="https:"+grid_product_div.find('img')['src'] 
        
        
        if Mars_printer.find_all("div", {"class": "grid-product__tag"}):
            grid_product=Mars_printer.find('div', attrs={'class':'grid-product__tag'}).text.replace('\n','').strip()
        else:
            grid_product=''
        product_title=Mars_printer.find('div', attrs={'class':'grid-product__title grid-product__title--body'}).text.replace('\n','').strip()
        product_price=Mars_printer.find('div', attrs={'class':'grid-product__price'}).text.replace('\n','').strip()
        href_list_now = Mars_printer.find('a', class_='grid-product__link').get('href')
        url_part = "https://www.elegoo.com"
        soup_under = get_page(url_part+href_list_now)
        all_editor = soup_under.find_all('div',class_="gryffeditor",id=False)
        for all_editor_each in all_editor:
            product_back_img = "https"+all_editor_each.find('div', attrs={'id':'m-1542790774641-0'}).find("img")["src"]
            small_slide_images = []
            small_slide_image_all = all_editor_each.find_all('img', attrs={'class':'gf_product-image-thumb'})
            for small_slide_image_each in small_slide_image_all:
                small_slide_images.append("https:"+small_slide_image_each['src'])
            part_gf_column = all_editor_each.find('div', attrs={'id':'c-1539334940899'})
            gf_product_title = part_gf_column.find('a').text;
            gf_product_price = part_gf_column.find('span', attrs={'class':'gf_product-price money'}).text
            gf_ul = part_gf_column.find('ul')
            gf_ul_b = gf_ul.find_all('b')
            Text_Block = []
            for gf_ul_b_each in gf_ul_b:
                Text_Block.append(gf_ul_b_each.text.replace('\xa0',''))
            if all_editor_each.find('div', attrs={'id':'e-1611571854570'}):
                Technical_Specification = all_editor_each.find('div', attrs={'id':'e-1611571854570'})
                Technical_Specifications = []
                if Technical_Specification.find_all("li"):
                    Technical_Specification_li = Technical_Specification.find_all('li')
                    for Technical_Specification_each in Technical_Specification_li:
                        Technical_Specifications.append(Technical_Specification_each.text.replace('\xa0',''))
            else:
                Technical_Specifications.append("")
            Shop_on_Amazons = []
            if all_editor_each.find('div', attrs={'id':'e-1608794733583'}):
                Shop_on_Amazon = all_editor_each.find('div', attrs={'id':'e-1608794733583'})
                Shop_on_Amazon_as = Shop_on_Amazon.find_all('a')
                for Shop_on_Amazon_a in Shop_on_Amazon_as:
                    if Shop_on_Amazon_a.text!="":
                        Shop_on_Amazons.append(Shop_on_Amazon_a.text)
            Resources = []
            if all_editor_each.find('div', attrs={'id':'r-1611628621780'}):
                Resource = all_editor_each.find('div', attrs={'id':'r-1611628621780'})
                Resource_ps = Resource.find_all('p')
                for Resource_p in Resource_ps:
                    if Resource_p.text!="":
                        Resources.append(Resource_p.text.replace('\xa0',''))
            Tips = []
            if all_editor_each.find('h6'):
                Tips_h6 = all_editor_each.find('h6')
                Tips_fonts = Tips_h6.find_all("font")
                for Tips_font in Tips_fonts:
                    Tips.append(Tips_font.text.replace('\xa0',''))
            descriptions = []
            if all_editor_each.find('div', attrs={'id':'e-1542792009192'}):
                description = all_editor_each.find('div', attrs={'id':'e-1542792009192'})
                description_lis = description.find_all('li')
                for description_li in description_lis:
                    if description_li.text!="":
                        descriptions.append(description_li.text)
            video_url = soup_under.select_one("iframe").attrs["src"]
            video_description = ""
            if all_editor_each.find('div', attrs={'id':'e-1608798867353'}):
                video_description = all_editor_each.find('div', attrs={'id':'e-1608798867353'}).text
            if all_editor_each.find('div', attrs={'id':'e-1623064870319'}):
                video_description = all_editor_each.find('div', attrs={'id':'e-1623064870319'}).text
            video_des_main = []
            video_des_title = []
            if all_editor_each.find('div', attrs={'id':'e-1623064870319'}):
                video_des_div = all_editor_each.find('div', attrs={'id':'e-1623064870319'})
                video_des_title.append(video_des_div.find('strong').text)
                video_des_ul = video_des_div.find('ul')
                video_des_spans = video_des_ul.find_all('li')
                for video_des_span in video_des_spans:
                    video_des_main.append(video_des_span.text.replace('\xa0',''))
            if not all_editor_each.find('div', attrs={'id':'r-1623232092049'}):
                if all_editor_each.find('div', attrs={'id':'e-1608798867353'}):
                    video_des_div = all_editor_each.find('div', attrs={'id':'e-1608798867353'})
                    if video_des_div.find('strong'):
                        video_des_title.append(video_des_div.find('strong').text)
                    if video_des_div.find('b'):
                        video_des_title.append(video_des_div.find('b').text)
                    if video_des_div.find('ul'):
                        video_des_ul = video_des_div.find('ul')
                        video_des_spans = video_des_ul.find_all('li')
                        for video_des_span in video_des_spans:
                            video_des_main.append(video_des_span.text.replace('\xa0',''))
            if all_editor_each.find('div', attrs={'id':'r-1623232092049'}):
                video_des_div = all_editor_each.find('div', attrs={'id':'r-1623232092049'})
                video_des_div_left = video_des_div.find('div', attrs={'id':'e-1608798867353'})
                video_des_title.append(video_des_div_left.find('b').text)
                video_des_ul_left = video_des_div_left.find('ul')
                video_des_spans_left = video_des_ul_left.find_all('li')
                for video_des_span_left in video_des_spans_left:
                    video_des_main.append(video_des_span_left.text.replace('\xa0','')+'first title')
                video_des_div_right = video_des_div.find('div', attrs={'id':'e-1608798867353'})
                video_des_title.append(video_des_div_right.find('b').text)
                video_des_ul_right = video_des_div_right.find('ul')
                video_des_spans_right = video_des_ul_right.find_all('li')
                for video_des_span_right in video_des_spans_right:
                    video_des_main.append(video_des_span_right.text.replace('\xa0','')+'second title')
            # print(video_des_title, video_des_main)
            gf_small_image_url = []
            if all_editor_each.find('div', attrs={'id':'r-1608798717635'}):
                gf_small_image_div = all_editor_each.find('div', attrs={'id':'r-1608798717635'})
                gf_small_image_urls = gf_small_image_div.find_all('img', attrs={'class':'gf_image'})
                for gf_small_image_url_each in gf_small_image_urls:
                    gf_small_image_url.append(gf_small_image_url_each['src'])
            if all_editor_each.find('div', attrs={'id':'c-1608796875990'}):
                gf_small_image_div = all_editor_each.find('div', attrs={'id':'c-1608796875990'})
                gf_small_image_urls = gf_small_image_div.find_all('img', attrs={'class':'gf_image'})
                for gf_small_image_url_each in gf_small_image_urls:
                    gf_small_image_url.append(gf_small_image_url_each['src'])
            if all_editor_each.find('div', attrs={'id':'r-1611643214359'}):
                gf_small_image_div = all_editor_each.find('div', attrs={'id':'r-1611643214359'})
                gf_small_image_urls = gf_small_image_div.find_all('img', attrs={'class':'gf_image'})
                for gf_small_image_url_each in gf_small_image_urls:
                    gf_small_image_url.append(gf_small_image_url_each['src'])
            if all_editor_each.find('div', attrs={'id':'c-1611627117787'}):
                gf_small_image_div = all_editor_each.find('div', attrs={'id':'c-1611627117787'})
                gf_small_image_urls = gf_small_image_div.find_all('img', attrs={'class':'gf_image'})
                for gf_small_image_url_each in gf_small_image_urls:
                    gf_small_image_url.append(gf_small_image_url_each['src'])
            if all_editor_each.find('div', attrs={'id':'r-1611743562907'}):
                gf_small_image_div = all_editor_each.find('div', attrs={'id':'r-1611743562907'})
                gf_small_image_urls = gf_small_image_div.find_all('img', attrs={'class':'gf_image'})
                for gf_small_image_url_each in gf_small_image_urls:
                    gf_small_image_url.append(gf_small_image_url_each['src'])
            if all_editor_each.find('div', attrs={'id':'r-1611804317079'}):
                gf_small_image_div = all_editor_each.find('div', attrs={'id':'r-1611804317079'})
                gf_small_image_urls = gf_small_image_div.find_all('img', attrs={'class':'gf_image'})
                for gf_small_image_url_each in gf_small_image_urls:
                    gf_small_image_url.append(gf_small_image_url_each['src'])
            if all_editor_each.find('div', attrs={'id':'r-1622459360659'}):
                gf_small_image_div = all_editor_each.find('div', attrs={'id':'r-1622459360659'})
                gf_small_image_urls = gf_small_image_div.find_all('img', attrs={'class':'gf_image'})
                for gf_small_image_url_each in gf_small_image_urls:
                    gf_small_image_url.append(gf_small_image_url_each['src'])
        dbname = get_database()
        collection_name = dbname["get_detail_page"]
        item = {
            "new_img" : grid_product_img_src,
            "product_img" : product_back_img,
            "grid_product" : grid_product,
            "product_title" : product_title,
            "product_price" : product_price,
            "gf_product_title" : gf_product_title,
            "gf_product_price" : gf_product_price,
            "small_slide_images" : small_slide_images,
            "gf_Text_Block" : Text_Block,
            "Technical_Specifications" : Technical_Specifications,
            "Shop_on_Amazons" : Shop_on_Amazons,
            "Resources" : Resources,
            "Tips" : Tips,
            "descriptions" : descriptions,
            "video_url" : video_url,
            "video_description" : video_description,
            "video_des_title" : video_des_title,
            "video_des_main" : video_des_main,
            "gf_small_image_url" : gf_small_image_url
        }
        collection_name.insert_many([item])
def main():
    url_main = "https://www.elegoo.com/collections/"
    proxy_host = "proxy.crawlera.com"
    proxy_port = "8011"
    proxy_auth = "bfd96677d6764ae0a273d342796328f9:" # Make sure to include ':' at the end
    proxies = {
        "https": f"http://{proxy_auth}@{proxy_host}:{proxy_port}/",
        "http": f"http://{proxy_auth}@{proxy_host}:{proxy_port}/"
    }

    headers = {
        'X-Crawlera-Region': 'PH'
    }
    last_urls = ['mars-series', 'saturn-series', 'neptune-series-fdm-printers', 'clean-cure-series', 'parts-accessories', 'resin']
    verify='zyte-proxy-ca.crt' 
    for last_url in last_urls:
        get_detail_page(get_page(url_main+last_url,proxies,headers,verify ))    

if __name__ == '__main__':
    main()

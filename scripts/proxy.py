import requests

response = requests.get(
    "https://httpbin.org/get",
    proxies={
        "http": "http://bfd96677d6764ae0a273d342796328f9:@proxy.crawlera.com:8011/",
        "https": "http://bfd96677d6764ae0a273d342796328f9:@proxy.crawlera.com:8011/",
    },
    verify='zyte-proxy-ca.crt' 
)
print(response.text)
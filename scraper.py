import requests
import re
from bs4 import BeautifulSoup
import time
import json


def extract_url(url):

    if url.find("www.amazon.in") != -1:
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://www.amazon.in" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://www.amazon.in" + url[index:index2]
            else:
                url = None
    else:
        url = None
    return url

def get_converted_price(price):
    converted_price = float(re.sub(r"[^\d.]", "", price))
    return converted_price

def get_page_soup(clean_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    page = requests.get(clean_url, headers=headers)
    return BeautifulSoup(page.content, "html5lib")

def extract_amazon_data(url):
    
    details = {"name": "", "price": 0, "deal": True, "url": "",'website':'amazon'}
    _url = extract_url(url)
    soup = get_page_soup(_url)
    title = soup.find(id="productTitle")
    price = soup.find(id="priceblock_dealprice")
    if price is None:
        price = soup.find(id="priceblock_ourprice")
        details["deal"] = False
    if title is not None and price is not None:
        details["name"] = title.get_text().strip()
        details["price"] = get_converted_price(price.get_text())
        details["url"] = _url
    return details

def  extract_myntra_data(url):
    details = {"name": "", "price": 0, "deal": False, "url": "",'website':'myntra'}
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    s = requests.Session()
    res = s.get(url, headers=headers)
    soup = BeautifulSoup(res.text,"lxml")
    script = None
    for s in soup.find_all("script"):
        if 'pdpData' in s.text:
            script = s.get_text(strip=True)
            break
    datadict = json.loads(script[script.index('{'):])
    if datadict['pdpData'].get('price').get('discounted'):
        details['price'] = datadict['pdpData'].get('price').get('discounted') 
        details['deal'] = True
    else:
        details['price'] =datadict['pdpData'].get('price').get('mrp')
    details['name'] = datadict['pdpData'].get('name')
    details['url'] = url.split('?')[0]
    return details

def extract_flipkart_data(url):
    details = {"name": "", "price": 0, "deal": False, "url": "",'website':'flipkart'}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html5lib")
    
        
    try:
        title = soup.find('h1',{'class':'yhB1nd'}).span
        price = soup.find('div',{'class':'_30jeq3 _16Jk6d'})
        offer_text = soup.find('div',{'class':'_1V_ZGU'}).span.text
        if 'special' in offer_text.lower():
            details["deal"] = True
    except:
        details['deal'] = False
    if title is not None and price is not None:
        details["name"] = title.get_text().strip()
        details["price"] = get_converted_price(price.get_text())
        details["url"] = url.split('?')[0]

    return details
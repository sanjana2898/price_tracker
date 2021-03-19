import requests 
from bs4 import BeautifulSoup
import re
import pandas as pd


details = {"name": "", "price": 0, "deal": False, "url": "",'website':'myntra'}
url='https://www.myntra.com/headphones/realme/realme-black-true-wireless-q-earbuds/13033472/buy'
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
s = requests.Session()
res = s.get(url, headers=headers)

soup = BeautifulSoup(res.text,"lxml")
print(res)
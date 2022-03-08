import requests as r
import csv
from bs4 import BeautifulSoup

url = 'https://www.copunderdog.com/shop/sneakers/jordans/air-jordan-1-low-canyon-rust/'
a = r.get(url).text

soup = BeautifulSoup(a, 'html.parser')


for i in soup.find_all('div'):
    if i.attrs == {'class': ['woocommerce-tabs', 'wc-tabs-wrapper']}:
        descendants = i.descendants
        for j in descendants:
            try:
                if j.attrs == {'class': ['woocommerce-Tabs-panel', 'woocommerce-Tabs-panel--description', 'panel', 'entry-content', 'wc-tab'], 'id': 'tab-description', 'role': 'tabpanel', 'aria-labelledby': 'tab-title-description'}:
                    Desc = j.text.strip()
            except:
                continue

print(Desc)
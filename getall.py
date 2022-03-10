import requests as r
import bS


url = 'https://www.copunderdog.com/wp-json/wc/store/products'

total_pages = int(r.head(url).headers['x-wp-totalpages'])
total_shoes = int(r.head(url).headers['x-wp-total'])

for i in range(1, total_pages+1):
    page = r.get(url+"?page=%d" %i).json()
    for i in range(10):
        page[i]['permalink']

bS.
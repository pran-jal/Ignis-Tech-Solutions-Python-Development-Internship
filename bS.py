import requests as r
import csv
from bs4 import BeautifulSoup

url = 'https://www.copunderdog.com/shop/sneakers/jordans/air-jordan-1-high-og-patent-bred/'
a = r.get(url).text

soup = BeautifulSoup(a, 'html.parser')

img_urls = []
for i in soup.find_all('div', attrs = {'class':['thumbnails']}): 
        for a in i.find_all('a', href=True):
            img_urls.append(a['href'])

for i in soup.find_all('div'):
    if i.attrs == {'class':['sticky-summary']}:
        descendants = i.descendants
        for j in descendants:
            try:
                if j.attrs == {'class': ['product_title', 'entry-title']}:
                    Name = j.text
                elif j.attrs == {'class': ['woocommerce-product-details__short-description']}:
                    Desc = j.text
                elif j.attrs == {'class': ['price']}:
                    Price = j.text.strip('₹').strip()
                elif j.attrs == {'class': ['variable-item-contents']}:
                    Value = j.text
                elif j.attrs == {'class': ['sku']}:
                    sktu = j.text
                elif j.attrs == {'class': ['posted_in']}:
                    categ = j.text
            except:
                continue

    if i.attrs == {'class': ['woocommerce-tabs', 'wc-tabs-wrapper']}:
        descendants = i.descendants
        for j in descendants:
            try:
                if j.attrs == {'class': ['woocommerce-Tabs-panel', 'woocommerce-Tabs-panel--description', 'panel', 'entry-content', 'wc-tab'], 'id': 'tab-description', 'role': 'tabpanel', 'aria-labelledby': 'tab-title-description'}:
                    Desc = j.text.strip()
            except:
                continue
    
brand = []
for a in soup.find_all('nav', attrs={'class':'woocommerce-breadcrumb breadcrumb'}) :
    for i in a.find_all('a'):
        brand.append(i.text)
brand = brand.pop()

f = open("test.csv", 'a', encoding='utf-8')
writer = csv.writer(f)
header = ['Item URL', 'Name', 'Price', 'Brand', 'Size', 'SKU', 'categories', 'Description', 'All images urls' ]
row = [url, Name, Price, brand, Value, sktu, categ.split('Categories: ')[1], Desc, ',\n'.join(img_urls) ]
# writer.writerow(header)
writer.writerow(row)
f.close()
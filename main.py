import requests as r
import os
import sys
import csv
from bs4 import BeautifulSoup as BS

class shoes():
    def __init__(self, url, json) :                      # initiates the object with empty values
        self.url = url  #
        self.name = ''  #
        self.price = '' #
        self.brand = '' #
        self.size = []  #
        self.sku = ''   #
        self.category = ''  #
        self.description = ''   #
        self.images = ''    #
        self.request(json=json)
        page = BS(r.get(url).text, 'html.parser')
        self.send_details(page, json)
        del page

    def request(self, json) :
        try :
            self.name = json['name']
        except :
            pass

        try:
            self.sku = json['sku']
        except :
            pass

        try:
            self.price = "%s %s" %( json['prices']['currency_prefix'], json['prices']['sale_price'] )
        except :
            pass
        try:
            self.brand = json['categories'][0]['name']
        except :
            pass
        try:
            self.description = ' '.join(json['short_description'].strip('</p>').split('</p>\n<p>'))
        except :
            pass

    def img_url(self, page, json) :                                               # gets product's images
        imag_url = []
        for i in json['images']:
            imag_url.append(i['src'])                                             # gets product's images
        for i in page.find_all('div', attrs = {'class':['thumbnails']}): 
            for a in i.find_all('a', href=True):
                imag_url.append(a['href'])
        self.images = ' ,\n'.join(imag_url)
        del imag_url

    def brands(self, page, ) :                                                 # gets product's brand
        brand = []
        for a in page.find_all('nav', attrs={'class':'woocommerce-breadcrumb breadcrumb'}) :
            for i in a.find_all('a'):
                brand.append(i.text)
        self.brand = brand.pop()
        del brand

    def num(self, number):
        if not number.isalpha() :
            if float(number)//1 == float(number)/1:
                return int(number)
            return float(number)
        return number

    def sizes(self, json) :
        try:
            for i in json['attributes'][0]['terms'] :
                self.size.append(self.num(i['name']))
        except:
            pass
    
    def get_details(self, page) :                                               # gets product's rest of the details
        for i in page.find_all('div'):
            if i.attrs == {'class':['sticky-summary']}:
                descendants = i.descendants
                for j in descendants:
                    try:
                        if j.attrs == {'class': ['product_title', 'entry-title']} and self.name == '':
                            self.name = j.text
                        elif j.attrs == {'class': ['woocommerce-product-details__short-description']} and self.description == '':
                            self.description = j.text.strip().strip('\n')
                        elif j.attrs == {'class': ['price']} and self.price == '':
                            self.price = j.text
                        elif j.attrs == {'class': ['variable-item-contents']} and self.size == []:
                            self.size = j.text
                        elif j.attrs == {'class': ['sku']} and self.sku == '':
                            self.sku = j.text
                        elif j.attrs == {'class': ['posted_in']} and self.category == '':
                            self.category = j.text.split('Categories: ')[1]
                    except:
                        continue

            if i.attrs == {'class': ['woocommerce-tabs', 'wc-tabs-wrapper']} and self.description == '':
                descendants = i.descendants
                for j in descendants:
                    try:
                        if j.attrs == {'class': ['woocommerce-Tabs-panel', 'woocommerce-Tabs-panel--description', 'panel', 'entry-content', 'wc-tab'], 'id': 'tab-description', 'role': 'tabpanel', 'aria-labelledby': 'tab-title-description'}:
                            self.description = j.text.strip().strip('\n')
                    except:
                        continue                
    
    def w_t_csv(self) :                                                             # writes details to a csv file
        f = open("shoes.csv", 'a', encoding='utf-8')
        writer = csv.writer(f)
        header = ['Item URL', 'Name', 'Price', 'Brand', 'Size', 'SKU', 'categories', 'Description', 'All images urls' ]
        row = [self.url, self.name, self.price, self.brand, self.size, self.sku, self.category, self.description, self.images ]
        # writer.writerow(header)
        writer.writerow(row)
        f.close()

    def send_details(self, page, json) :
        self.img_url(page, json)
        self.brands(page)
        self.sizes(json)
        self.get_details(page)
        self.w_t_csv()




def main() :
    argv = sys.argv
    if 'copunderdog' not in argv and 'www.copunderdog.com' not in argv and 'copunderdog.com' not in argv and 'https://www.copunderdog.com' not in argv:
        print("Invalid name\nTry 'copunderdog.com' ")
        return
    
    url = 'https://www.copunderdog.com/wp-json/wc/store/products'
    total_pages = int(r.head(url).headers['x-wp-totalpages'])
    
    print('creating shoes.csv')
    try:
        os.remove('shoes.csv')                                  # del previous .csv file
    except:
        pass

    f = open("shoes.csv", 'a', encoding='utf-8')            # to initialize the .csv file
    writer = csv.writer(f)
    header = ['Item URL', 'Name', 'Price', 'Brand', 'Size', 'SKU', 'categories', 'Description', 'All images urls' ]
    writer.writerow(header)
    f.close()

    for j in range(1, total_pages+1):
        page = r.get(url+"?page=%d" %j).json()
        print('Writing page %d of %d\n'%(j, total_pages))
        for i in page:
            shoe_link = i['permalink']
            if shoe_link.split('/')[4] == 'sneakers':
                shoe_details = shoes(shoe_link, i)
                del shoe_details

if __name__ == '__main__':
    main()

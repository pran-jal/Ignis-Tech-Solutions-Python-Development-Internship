import requests as r
from bs4 import BeautifulSoup
from html.parser import HTMLParser as parser

class HTML(parser):
    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.reset()
        self.found = 0
        self.brand = 0
        self.a = 0
        self.img_url = 0

        self.brands = []
        self.img_urls = []
        self.details = {}


    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'div':
            for i,j in attrs:
                if i == 'class':

                    if j == 'summary entry-summary':
                        self.found = 1

                    elif j == 'woocommerce-tabs wc-tabs-wrapper':
                        self.found = 0

                    elif j == 'thumbnails':
                        self.img_url = 1

                    elif j == 'product-summary clearfix':
                        self.brand = 0 

                    elif (j == 'woocommerce-product-gallery__image active' or j == 'woocommerce-product-gallery__image ') and self.img_url:
                        self.a = 1
                    
                    elif j == 'woocommerce-product-details__short-description' :
                        self.details['desc'] = 'ok'

        elif tag.lower() == 'a' and self.a :
            for i,j in attrs:
                if i == 'href':
                    self.img_urls.append(j)
                    self.a = 0
            
        elif tag.lower() == 'h1':
            for i,j in attrs:
                if i == 'class' and j == 'product_title entry-title':
                    self.details['Name'] = 'ok'

        
        elif tag.lower() == 'nav':
            for i,j in attrs:
                if i == 'class' and j == 'woocommerce-breadcrumb breadcrumb':
                    self.brand = 1

    def handle_endtag(self, tag):
        if tag.lower() == 'figure':
            self.img_url = 0
            self.a = 0

    def handle_data(self, data: str):
        if self.brand:
            self.brands.append(data)
        
        for i in self.details:
            if  self.details[i] == 'ok':
                self.details[i] = data

url = 'https://www.copunderdog.com/shop/sneakers/jordans/air-jordan-1-low-shadow-2-0/'
a = r.get(url).text
reader = HTML()
reader.feed(a)
reader.close()


print(reader.brands)
print(reader.img_urls)

# soup = BeautifulSoup(a, 'html.parser')

# def img_urls() :
#     for i in soup.find_all('div', attrs={'class':'thumbnails'}): 
#             for a in i.find_all('a', href=True):
#                 print(a['href'])

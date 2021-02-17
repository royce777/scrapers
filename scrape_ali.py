import requests
from bs4 import BeautifulSoup
import csv

def get_price(s,url):
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    page = requests.get(url, headers=HEADERS)
    #print(page.content)
    soup = BeautifulSoup(page.content, "lxml")
    name = soup.find(class_="text").get_text().strip()
    # sometimes there isn't a priceblock with "ourprice" id, cause it's in sale
    try:
        price = float(soup.find(id='priceblock_ourprice').get_text())
    except:
        # this part gets the price in dollars from amazon.com store
        try:
            price = float(soup.find(id='priceblock_saleprice').get_text())
        except:
            price = ''
    print(name, price)



with open('products.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)

    for row in reader:
        with requests.Session() as s:
            get_price(s, row[0])


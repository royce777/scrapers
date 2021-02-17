import http.cookiejar, urllib.request, sys, csv
from bs4 import BeautifulSoup


def get_data(url, out_writer):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    page = opener.open(url)
    page.addheaders = [('User-agent', 'Mozilla/5.0')]
    soup = BeautifulSoup(page, "lxml")
    name = soup.find(id="productTitle").get_text().strip()
    try:
        price = soup.find(id='priceblock_ourprice').get_text()
    except:
        try:
            price = soup.find(id='priceblock_dealprice').get_text()
        except:
            price = 'NA'
    out_writer.writerow([name,price])

with open('amazon_prices.csv', mode = 'w') as out_file:
    out_writer = csv.writer(out_file, delimiter = ',')
    with open('amazon_products.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            get_data(row[0], out_writer)


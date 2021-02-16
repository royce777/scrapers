import http.cookiejar, urllib.request, sys
from bs4 import BeautifulSoup


def get_data(url):
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
            price = soup.find(id='priceblock_saleprice').get_text()
        except:
            price = 'NA'
    print(name, price)
    with open('test.txt', 'w') as f:
        sys.stdout = f # Change stdout to get all the html for testing purposes.
        print (page.read())
        sys.stdout = original_stdout # Reset stdout


original_stdout = sys.stdout # save ref to default stdout

for i in sys.argv[1:]:
    get_data(i)
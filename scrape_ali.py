import requests, sys, csv, json, pprint
from subprocess import check_output
from bs4 import BeautifulSoup

def get_data(url, out_writer):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')
    for script in soup.find_all('script'):
        if "runParams" in str(script):
            clean_script = script.text.strip()
            #print(clean_script)
            with open('temp.js','w') as f:
                f.write('window = {};\n'+clean_script+';\nprocess.stdout.write(JSON.stringify(window.runParams));')
            window_runParams = check_output(['node','temp.js'])
            data_json = json.loads(window_runParams)
            try:
                price = data_json['data']['middleBannerModule']['uniformMiddleBanner']['price']
            except:
                try:
                    price = data_json['data']['priceModule']['formatedActivityPrice']
                except:
                    price = data_json['data']['priceModule']['formatedPrice']
            name = data_json['data']['pageModule']['title']
            out_writer.writerow([name, price])

with open('ali_prices.csv', mode = 'w') as out_file:
    out_writer = csv.writer(out_file, delimiter = ',')
    with open('ali_products.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            get_data(row[0], out_writer)

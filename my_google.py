# -*- coding: utf-8 -*-
from urllib import request, parse
import urllib
import http.cookiejar
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import os


headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
         "Referer": "https://www.google.com.hk/"}


cjar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))

headall=[]
for key, value in headers.items():
    item = (key, value)
    headall.append(item)
opener.addheaders=headall
urllib.request.install_opener(opener)

csvfile_names = os.listdir('.\\URL_GOOGLE_CSV')

txtfile = open('google_results.txt', 'a+', encoding='utf-8')

for csvfile_name in csvfile_names:
    stock_name = csvfile_name.split('.')[0]
    stock_name = stock_name.split('_')[-1]
    txtfile.write(stock_name)
    txtfile.write('\n')
    txtfile.flush()

    csvfile_path = '.\\URL_GOOGLE_CSV\\' + csvfile_name
    # print(csvfile_path)
    csvfile = pd.read_csv(csvfile_path, encoding='unicode_escape', sep='\n')
    urls_np = csvfile.values
    urls = [url[0] for url in urls_np]

    for i, url in enumerate(urls):
        print(url)
        txtfile.write(str(url) + '\n')
        txtfile.flush()
        data = urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(data, 'html.parser')
        results = soup.find_all('div', id='resultStats')
        for result in results:
            s = result.get_text()  # str
            writer = str(i) + ' ' + s + '\n'
            print(writer)
            txtfile.write(writer)
            txtfile.flush()
        time.sleep(3 + 2*random.random())

txtfile.close()

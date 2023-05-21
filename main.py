import openpyxl as openpyxl
import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

url1 = "https://www.trendyol.com/apple-laptop-x-b101470-c103108"

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}



def make_req(url):

    page = requests.get(url, headers=headers)
    html_page = BeautifulSoup(page.content, "html.parser")

    return html_page

def title(url):

    title_list = []
    titles = make_req(url)

    for title in titles.find_all("span"):
        found_title = title.get("title")

        if found_title:
            title_list.append(found_title)

    temiz_liste = [eleman.replace("'", "").replace(",", "") if eleman is not None else "" for eleman in title_list]
    en_temiz_list =[]

    for i in range(0, len(temiz_liste), 2):

        combined = temiz_liste[i] + title_list[i + 1]
        en_temiz_list.append(combined)

    return en_temiz_list


    return temiz_liste

def price(url):

    price_list = []
    prices = make_req(url)

    for price in prices.find_all("div", class_ = "prc-box-dscntd"):

        if price:
            price_list.append(price.text)

    return price_list


sonuc = dict(zip(title(url1), price(url1)))

df = pd.DataFrame.from_dict(sonuc, orient='index', columns=['Fiyat'])
df.index.name = 'Ürün'

df.to_excel('veriler.xlsx', index=True)
print(df)


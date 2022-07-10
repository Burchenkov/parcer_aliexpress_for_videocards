from cgitb import text
from types import NoneType
import requests
from bs4 import BeautifulSoup
import csv
import json
from lxml import etree
from fake_useragent import UserAgent

# Init constant
UA = UserAgent()
HOST = 'https://sbermegamarket.ru/'
URL = 'https://aliexpress.ru/category/202001171/graphics-cards/w-%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BA%D0%B0%D1%80%D1%82%D1%8B?spm=a2g2w.productlist.0.0.7d165edeEfjznm'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': UA.random
} 
MAX_NUM = 99999


# write main def
def main(url):
    # creating csv file and write start row into it 
    with open('cards_list.csv', 'w', newline = '', encoding = 'utf-8') as file:
        writer = csv.writer(file, delimiter = ' ')
        writer.writerow((
            'Title videocards',
            'Current price',
            'Old price',
            'Discount'
        ))
    # main cycle to turn pages
    for k in range(1, MAX_NUM):
        # getting html
        req = requests.get(url, headers = HEADERS, params = {'page': k} , timeout = 30)
        src = req.text

        # reading and writing received html
        with open('index.html', 'w', encoding = 'utf-8') as file:
            file.write(src)
        with open('index.html', 'r', encoding = 'utf-8') as file:
            html = file.read()

        soup = BeautifulSoup(html, 'lxml')
        cards = soup.find_all('div', class_ = 'product-snippet_ProductSnippet__content__tusfnx')
        print(f'Page num:{k} parcing now')
        # condition for pagination
        if type(soup.find('div', class_ = 'SearchWrap_SearchError__errorContainer__oy8dw')) == NoneType:
            cards_dict = []
            for i in cards:
                try: 
                    cards_discount = i.find('div', class_ = ('snow-price_SnowPrice__discountPercent__2y0jkd')).text
                    # condition for searching only cards at a discount
                    if int(i.find('div', class_ = ('snow-price_SnowPrice__discountPercent__2y0jkd')).text.replace('-','').replace('%','')) >= 45:
                        cards_name = i.find('div', class_ = 'product-snippet_ProductSnippet__name__tusfnx').text
                        cards_new_price = i.find('div', class_ = 'snow-price_SnowPrice__mainM__2y0jkd').text
                        cards_old_price = i.find('div', class_ = 'snow-price_SnowPrice__secondPrice__2y0jkd').text
                        cards_discount = i.find('div', class_ = ('snow-price_SnowPrice__discountPercent__2y0jkd')).text

                        cards_dict.append({
                            cards_name,
                            cards_new_price,
                            cards_old_price,
                            cards_discount
                        })
                        # add soup objects to csv file
                        with open('cards_list.csv', 'a', newline = '' , encoding = 'utf-8') as file:
                            writer = csv.writer(file, delimiter = ' ')
                            writer.writerow((
                                cards_name,
                                cards_new_price, 
                                cards_old_price, 
                                cards_discount
                                ))
                            
                except AttributeError:
                    continue
        else:
            print('Parsing pages are over')
            break


if __name__ == '__main__':
    main(URL)  
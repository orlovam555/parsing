import requests
from bs4 import BeautifulSoup
import json


def get_data():
    books = []
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    url1 = "https://www.labirint.ru/genres/2308/"
    count_books = 0
    response = requests.get(url=url1, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    pages_count = int(soup.find('div', class_="pagination-numbers").find_all('a')[-1].text)
    for page in range(1, pages_count + 1):
        url = f"https://www.labirint.ru/genres/2308/?display=table&page={page}"
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        books_items = soup.find("tbody", class_="products-table__body").find_all("tr")
        for k, item in enumerate(books_items):
            try:
                title = item.find("td", class_="col-sm-4").text.strip()
            except:
                title = '-'
            try:
                author = item.find("td", class_="col-sm-2").text.strip()
            except:
                author= '-'
            try:
                price_after = item.find("span", class_="price-val").text.strip()
            except:
                price_after= '-'
            try:
                price_before = item.find("span", class_="price-old").text.strip()
            except:
                price_before= '-'
            try:
                sell = item.find("span", class_="price-val")["title"].strip()
            except:
                sell='-'
            a = item.find("td", class_="col-sm-4").find("a")["href"]
            url = f"https://www.labirint.ru{a}"
            count_books+=1
            books.append(
                {
                    'title': title,
                    'author': author,
                    'price_before': price_before,
                    'price_after': price_after,
                    'sell': sell,
                    'url': url
                }
            )
            m = url1.split('/')[-2]
            with open(f'labirint.{m}', 'w', encoding="UTF-8") as file:
                json.dump(books, file, indent=4, ensure_ascii=False)
    print(f'всего книг собрали {count_books}')

get_data()


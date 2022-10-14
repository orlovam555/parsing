import requests
from bs4 import BeautifulSoup
import json
import time
from openpyxl.workbook import Workbook

def get_data_html(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    return soup

def get_books(url):
    books = []
    html_for_number_page = get_data_html(url)
    pages_count = int(html_for_number_page.find('div', class_="pagination-number__right").find('a').text)
    count_books = 0
    for page in range(1, 3):
        url_page = f"{url}?display=table&page={page}"
        soup = get_data_html(url_page)
        books_items = soup.find("tbody", class_="products-table__body").find_all("tr")
        for k, item in enumerate(books_items):
            try:
                title = item.find("td", class_="col-sm-4").text.strip()
            except:
                title = 0
            try:
                author = item.find("td", class_="col-sm-2").text.strip()
            except:
                author = 0
            try:
                price_after = item.find("span", class_="price-val").text.strip()
                price_after = int(price_after.replace('₽','').replace(' ',''))
            except:
                price_after = 0
            try:
                price_before = item.find("span", class_="price-old").text.strip()
                price_before = int(price_before.replace(' ',''))
            except:
                price_before = 0
            try:
                sell = int(item.find("span", class_="price-val")["title"].strip().split()[0][1:-1])
            except:
                sell = 0
            a = item.find("td", class_="col-sm-4").find("a")["href"]
            url_book = f"https://www.labirint.ru{a}"
            count_books+=1
            books.append(
                {
                    'title': title,
                    'author': author,
                    'price_before': price_before,
                    'price_after': price_after,
                    'sell': sell,
                    'url': url_book
                }
            )
        m = url.split('/')[-2]
        books.append(m)
        print(f'Всего книг собрали {count_books}')
        print(f'Категория {m}')
        return books

def save_json(data: list):
    file_name = get_file_name(data[-1]) + '.json'
    with open(file_name, 'w', encoding="UTF-8") as file:
        json.dump(data[:-1], file, indent=4, ensure_ascii=False)

def save_excel(data):
    headers = list(data[0].keys())
    file_name = get_file_name(data[-1]) + '.xlsx'

    wb = Workbook()
    page = wb.active
    page.title = 'data'
    page.append(headers)
    for book in data[:-1]:
        row = []
        for k, v in book.items():
            row.append(v)
        page.append(row)
    wb.save(filename=file_name)


def get_file_name(m):
    return time.strftime("%m_%d_%Y_%H_%M") + '_' + m

def main(url):
    books_data = get_books(url)
    #save_json(books_data)
    save_excel(books_data)


if __name__ == '__main__':
    main('https://www.labirint.ru/genres/2308/')




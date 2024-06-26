import requests
from bs4 import BeautifulSoup
import csv

# URL страницы, которую будем парсить
url = "https://www.market-sveta.ru/category/ljustry-podvesnye/"

# Заголовки для HTTP-запроса
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


# Функция для парсинга страницы
def parse_page(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    for product in soup.select('div.sw-show-gall.sw-gall'):
        name = product.select_one('img')['title']
        price = product.select_one('div.price').get_text(strip=True)  # Найдите правильный селектор для цены
        link = product.select_one('a')['href']
        link = requests.compat.urljoin(url, link)  # Преобразуем относительную ссылку в абсолютную

        products.append({
            'name': name,
            'price': price,
            'link': link
        })

    return products


# Функция для парсинга всех страниц с учетом пагинации
def parse_all_pages(start_url):
    all_products = []
    current_url = start_url

    while current_url:
        print(f"Parsing {current_url}")
        products = parse_page(current_url)
        all_products.extend(products)

        # Найти ссылку на следующую страницу
        response = requests.get(current_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        next_page = soup.select_one('a.next')
        if next_page:
            current_url = requests.compat.urljoin(current_url, next_page['href'])
        else:
            current_url = None

    return all_products


# Парсим все страницы
products = parse_all_pages(url)

# Сохраняем данные в CSV
with open('products.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['name', 'price', 'link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for product in products:
        writer.writerow(product)

print("Parsing completed. Data saved to products.csv.")
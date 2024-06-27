import requests
from bs4 import BeautifulSoup
import csv

# URL страницы для парсинга
url = 'https://www.divan.ru/category/svet'

# Заголовки для HTTP-запроса
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Выполнение HTTP-запроса
response = requests.get(url, headers=headers)
response.raise_for_status()

# Создание объекта BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Поиск информации о товарах
items = soup.find_all('div', class_='lsooF')  # Замените 'product-card' на нужный класс

# Создание CSV файла
with open('products.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название', 'Цена', 'Ссылка'])

    for item in items:
        name = item.find('a', class_='ui-GPFV8').text.strip()  # Замените 'product-name' на нужный класс
        price = item.find('span', class_='ui-LD-ZU').text.strip()  # Замените 'product-price' на нужный класс
        link = item.find('a', class_='ui-GPFV8')['href']  # Замените 'product-link' на нужный класс

        # Запись данных в CSV
        writer.writerow([name, price, f'https://www.divan.ru{link}'])

print('Данные успешно сохранены в файл products.csv')

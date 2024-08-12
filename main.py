import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1 Генерация и визуализация случайных данных.
def generate_and_visualize_random_data():
    # Параметры нормального распределения
    mean = 0       # Среднее значение
    std_dev = 1    # Стандартное отклонение
    num_samples = 1000  # Количество образцов

    # Генерация случайных чисел, распределенных по нормальному распределению
    data = np.random.normal(mean, std_dev, num_samples)

    # Построение гистограммы
    plt.figure(figsize=(8, 6))
    plt.hist(data, bins=30, alpha=0.7, edgecolor='black')
    plt.title('Гистограмма случайных данных\n(нормальное распределение)')
    plt.xlabel('Значения')
    plt.ylabel('Частота')
    plt.grid(True)
    plt.show()

# 2 Генерация двух наборов случайных данных для диаграммы рассеяния
    x = np.random.rand(100)
    y = np.random.rand(100)

    # Построение диаграммы рассеяния
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, alpha=0.7, edgecolors='w')
    plt.title('Диаграмма рассеяния двух наборов случайных данных')
    plt.xlabel('Набор данных X')
    plt.ylabel('Набор данных Y')
    plt.grid(True)
    plt.show()

# 3 Парсинг цен на диваны с сайта и анализ данных.
def parse_and_analyze_sofa_prices():
    # URL страницы для парсинга
    url = 'https://www.divan.ru/category/divany-i-kresla'

    # Заголовки для запроса
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Запрос страницы
    response = requests.get(url, headers=headers)

    # Проверка успешности запроса
    if response.status_code != 200:
        print(f"Ошибка при получении данных с {url}: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Убедитесь, что CSS-селектор соответствует элементам, которые вы хотите собрать
    divans = soup.select('div.VHx4T')  # Поменяйте на актуальный селектор

    data = []
    for divan in divans:
        name = divan.select_one('div.lsooF span')
        price = divan.select_one('div.q5Uds span')
        url = divan.select_one('a')

        # Проверка на существование элементов и их содержимого
        name_text = name.get_text(strip=True) if name else None
        price_text = price.get_text(strip=True) if price else None
        url_href = requests.compat.urljoin(response.url, url['href']) if url else None

        # Проверяем, что цена действительно является числом
        try:
            # Преобразование цены в числовой формат
            price_value = float(price_text.replace('₽', '').replace(' ', ''))
            data.append({
                'name': name_text,
                'price': price_value,
                'url': url_href
            })
        except (ValueError, AttributeError):
            # Пропускаем записи, где цена не может быть преобразована
            continue

    # Создание DataFrame
    df = pd.DataFrame(data)

    # Сохранение в CSV
    df.to_csv('divan_prices.csv', index=False)

    # Вычисление средней цены
    average_price = df['price'].mean()
    print(f'Средняя цена на диваны: {average_price:.2f} рублей')

    # Построение гистограммы цен
    plt.figure(figsize=(10, 6))
    plt.hist(df['price'], bins=20, alpha=0.7, edgecolor='black')
    plt.title('Гистограмма цен на диваны')
    plt.xlabel('Цена (рубли)')
    plt.ylabel('Частота')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Вызов функции для генерации и визуализации случайных данных
    generate_and_visualize_random_data()

    # Вызов функции для парсинга и анализа данных
    parse_and_analyze_sofa_prices()

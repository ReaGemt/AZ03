import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from time import sleep
from requests.exceptions import RequestException

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_page(url, headers, retries=3, backoff_factor=0.3):
    """
    Функция для загрузки страницы с повторными попытками в случае ошибки.
    """
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response
            else:
                logging.warning(
                    f"Ошибка {response.status_code} при получении данных с {url}. Попытка {attempt + 1} из {retries}.")
        except RequestException as e:
            logging.error(f"Ошибка запроса: {e}. Попытка {attempt + 1} из {retries}.")
        sleep(backoff_factor * (2 ** attempt))  # Экспоненциальная задержка
    logging.error(f"Не удалось получить данные с {url} после {retries} попыток.")
    return None


# 1 Генерация и визуализация случайных данных.
def generate_and_visualize_random_data():
    # Параметры нормального распределения
    mean = 0  # Среднее значение
    std_dev = 1  # Стандартное отклонение
    num_samples = 1000  # Количество образцов

    # Генерация случайных чисел, распределенных по нормальному распределению
    data = np.random.normal(mean, std_dev, num_samples)

    # Использование встроенного стиля 'ggplot'
    plt.style.use('ggplot')

    # Построение гистограммы
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=30, color='skyblue', alpha=0.7, edgecolor='black')
    plt.title('Гистограмма случайных данных\n(нормальное распределение)', fontsize=14, fontweight='bold')
    plt.xlabel('Значения', fontsize=12)
    plt.ylabel('Частота', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True)
    plt.show()

    # 2 Генерация двух наборов случайных данных для диаграммы рассеяния
    x = np.random.rand(16)
    y = np.random.rand(16)

    # Улучшение стиля диаграммы рассеяния
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='purple', alpha=0.7, edgecolors='w', s=70)
    plt.title('Диаграмма рассеяния двух наборов случайных данных', fontsize=14, fontweight='bold')
    plt.xlabel('Набор данных X', fontsize=12)
    plt.ylabel('Набор данных Y', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
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
    response = fetch_page(url, headers)
    if not response:
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Убедитесь, что CSS-селектор соответствует элементам, которые вы хотите собрать
    divans = soup.select('div._Ud0k')  # Проверьте и обновите селектор

    data = []
    for divan in divans:
        # Извлечение информации о диванах
        name = divan.select_one('div.lsooF span')
        price = divan.select_one('div.pY3d2 span')
        link = divan.select_one('a')

        # Проверка на существование элементов и их содержимого
        name_text = name.get_text(strip=True) if name else None
        price_text = price.get_text(strip=True) if price else None
        url_href = link['href'] if link else None

        # Проверяем, что цена действительно является числом
        if price_text:
            try:
                # Преобразование цены в числовой формат
                price_value = float(price_text.replace('руб.', '').replace(' ', '').replace(',', '.'))
                data.append({
                    'name': name_text,
                    'price': price_value,
                    'url': url_href
                })
            except ValueError:
                logging.warning(f"Невозможно преобразовать цену: {price_text}")
                continue

    # Проверка, удалось ли собрать данные
    if not data:
        logging.error("Данные не были собраны. Проверьте селекторы и структуру HTML.")
        return

    # Создание DataFrame
    df = pd.DataFrame(data)

    # Проверка на наличие столбца 'price'
    if 'price' not in df.columns:
        logging.error("Столбец 'price' отсутствует в DataFrame.")
        return

    # Сохранение в CSV
    df.to_csv('divan_prices.csv', index=False)

    # Вычисление средней цены
    average_price = df['price'].mean()
    logging.info(f'Средняя цена на диваны: {average_price:.2f} рублей')

    # Улучшение стиля гистограммы цен
    plt.figure(figsize=(10, 6))
    plt.hist(df['price'], bins=20, color='salmon', alpha=0.7, edgecolor='black')
    plt.axvline(average_price, color='blue', linestyle='dashed', linewidth=2,
                label=f'Средняя цена: {average_price:.2f} руб.')
    plt.title('Гистограмма цен на диваны', fontsize=14, fontweight='bold')
    plt.xlabel('Цена (рубли)', fontsize=12)
    plt.ylabel('Частота', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Вызов функции для генерации и визуализации случайных данных
    generate_and_visualize_random_data()

    # Вызов функции для парсинга и анализа данных
    parse_and_analyze_sofa_prices()

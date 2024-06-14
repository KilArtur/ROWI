import logging
import os
import sys
import json
import telegram
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)


# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Привет! Я бот для поиска товаров на Wildberries.\n'
        'Используйте команду /search для поиска товара по артикулу.\n'
        'Пример: велосипед детский 145296859 \n '
        'Вводите интересующий ваш товар и артикул через пробел'
    )

def check_and_split(product: str) -> (str, int):
    """
    Функция для проверки запроса на валидность и разделение на название товара и артикула

    :param product: строка с товаром и артиклем
    :return: название товара для поисковой строки и артикул
    """
    # Строка должна разбиваться минимум на 2 части
    if len(product.split()) < 2:
        logger.error(f"Запрос должен содерджать название товара и артикул через пробел")
        return None

    # последняя часть должна быть артикулом
    try:
        article = int(product.split()[-1])
    except ValueError:
        logger.error("Некорректный артикул. Артикул должен быть числом.")
        return None

    name = ' '.join(product.split()[:-1])
    return name, article


# Команда /search
def search(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.strip()
    command_parts = user_message.split(maxsplit=1)

    if len(command_parts) < 2:
        update.message.reply_text("Неверный формат запроса. Пример: /search велосипед детский 145296859")
        return

    name, article = check_and_split(command_parts[1])

    if name is None or article is None:
        return

    answer = {
        'page': None,
        'position': None
    }

    # Ограничение в первые 50 страниц
    for number_page in range(1, 51):
        params = {
            'ab_testing': 'false',
            'appType': '1',
            'curr': 'rub',
            'dest': '-369516',
            'page': number_page,
            'query': name,
            'resultset': 'catalog',
            'sort': 'popular',
            'spp': '30',
            'suppressSpellcheck': 'false',
            'uclusters': '0'
        }

        response = requests.get(API_URL, headers=headers, params=params)

        if response.status_code == 200:
            try:
                json_data = response.json()

                if 'data' in json_data and 'products' in json_data['data']:
                    products = json_data['data']['products']
                    for i, product in enumerate(products, start=1):
                        if product['id'] == article:
                            answer['page'] = params['page']
                            answer['position'] = i
                            break
            except json.JSONDecodeError:
                logger.warning('Ответ не является JSON')
        else:
            logger.error(f'Ошибка: {response.status_code}')

        if answer['page'] is not None and answer['position'] is not None:
            update.message.reply_text(f"Ваш продукт на странице {answer['page']}, месте {answer['position']}")
            return

    update.message.reply_text("Продукт не найден.")




if __name__ == '__main__':
    API_URL = 'https://search.wb.ru/exactmatch/ru/common/v5/search'

    headers = {
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Origin": "https://www.wildberries.ru",
        "Referer": "https://www.wildberries.ru/catalog/0/search.aspx",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0 (Edition Yx GX)",
        "sec-ch-ua": "\"Opera GX\";v=\"109\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "x-queryid": "qid82796597171809471720240613112848",
        "x-userid": "131290320"
    }
    # Включаем логирование
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stdout)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    # Загрузка переменных окружения из .env файла
    load_dotenv()
    TOKEN = os.getenv('TOKEN')

    # Отладка
    logger.info(f"Используемый токен: {TOKEN}")

    try:
        updater = Updater(TOKEN)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("search", search))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, search))

        updater.start_polling()
        updater.idle()
    except telegram.error.InvalidToken:
        logger.error("Предоставленный токен недействителен")
        exit(1)

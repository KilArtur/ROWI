import requests
import logging
import sys
import json


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

name_and_article = 'нож складной туристический 156416424'

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

name, article = check_and_split(name_and_article)

# Правильный URL для API, возвращающий JSON
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

# Ограничение в первые 50 страниц
for number_page in range(1, 51):
    # Параметры запроса
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

    # Выполнение GET-запроса к API
    response = requests.get(API_URL, headers=headers, params=params)

    # Печать деталей запроса

    # Проверка успешности запроса и печать JSON-данных
    if response.status_code == 200:
        try:
            json_data = response.json()  # Получаем JSON как словарь
            # json_data = json.dumps(json_data, indent=4, ensure_ascii=False)
            for i in range(99):
                if json_data['data']['products'][i]['id'] == article:
                    print(f"Ваш продукт на {params['page']} странице, {i + 1} месте")
                # logger.info(json_data['data']['products'][i]['id'])
            # list_article = []
            # for number in range(99):
            #     list_article.append(['data']['products'][number]['id'])
            # logger.info(list_article)
        except json.JSONDecodeError:
            logger.warning('Ответ не является JSON')
    else:
        logger.error(f'Ошибка: {response.status_code}')


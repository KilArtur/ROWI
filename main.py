import requests
import logging
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


KEY = 'P98qBimrXDymMDV9x9tMcqHBDJBHP8cK'
START_DATE = '2022-01-01'
END_DATE = '2022-01-07'

url_history = "https://api.apilayer.com/currency_data/historical"  # Получение данных на дату

headers= {
  "apikey": KEY
}

def get_currency(date):
    """
    Функция для получения данных на определенную дату

    :param date: Дата в формате 'YYYY-MM-DD'
    :return: Словарь данных о курсах валют  в формате JSON
    """
    params = {
        'date': date
    }
    response = requests.get(url_history, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Ошибка при получении данных: {response.status_code}")
        return None

def create_table(start_date, end_date):
    """

    :param start_date: Начальная дата периода в формате 'YYYY-MM-DD'
    :param end_date: Финаьная дата периода в формате 'YYYY-MM-DD'
    :return: Таблица (pandas), в которой по строкам - даты (01.01.2022-07.01.2022),
             а по столбцам названия из json (первые 10). На пересечении значение на дату
    """
    dates = pd.date_range(start=start_date, end=end_date)
    columns = sorted(get_currency(start_date)['quotes'].keys())[:10]
    df = pd.DataFrame(index=dates, columns=columns)
    return df


def pack_table(df):
    """
    Функция заполняет NaN значения в таблице, созданной в create_table

    :param df: Пустая таблица pandas созданная в create_table
    :return: Заполненная аблица (pandas), в которой по строкам - даты (01.01.2022-07.01.2022),
             а по столбцам названия из json (первые 10). На пересечении значение на дату
    """
    for date in df.index:
        currency_data = get_currency(date.strftime('%Y-%m-%d'))
        if currency_data is not None and 'quotes' in currency_data:
            for column in df.columns:
                if column in currency_data['quotes']:
                    df.loc[date, column] = currency_data['quotes'][column]
        else:
            logger.warning(f"Данные на дату {date.strftime('%Y-%m-%d')} не были получены или некорректны.")
    return df


print(pack_table(create_table(START_DATE, END_DATE)))
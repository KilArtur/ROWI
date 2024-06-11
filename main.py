import os
import logging
import requests
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext
)
from dotenv import load_dotenv

# Функция старта
def start(update: Update, context: CallbackContext) -> None:
    """
    Функция обрабатывает команду /start и отправляет пользователю приветственное сообщение

    :param update: Объект, содержащий информацию о текущем обновлении
    :param context: Контекст, содержащий данные о состоянии и бот API
    :return: None
    """
    update.message.reply_text(
        'Привет! Я валютный бот. Используйте команду /rate [currency], чтобы узнать текущий курс валюты к рублю.\n'
        'Поддерживаемые базовые валюты: USD, EUR'
    )

# Функция для получения курса валют
def rate(update: Update, context: CallbackContext) -> None:
    """
    Функция обрабатывает команду /rate и отправляет пользователю текущий курс указанной валюты к рублю

    :param update: Объект, содержащий информацию о текущем обновлении
    :param context: Контекст, содержащий данные о состоянии и бот API
    :return: None
    """
    if len(context.args) != 1:
        update.message.reply_text('Пожалуйста, укажите одну валюту. Например: /rate USD')
        return

    currency = context.args[0].upper()
    if currency not in ['USD', 'EUR']:
        update.message.reply_text('Поддерживаемые валюты: USD, EUR')
        return

    url = f'https://v6.exchangerate-api.com/v6/{KEY}/pair/{currency}/{BASE_CURRENCY}'
    response = requests.get(url)
    if response.status_code != 200:
        update.message.reply_text('Ошибка при получении данных. Попробуйте позже.')
        return

    data = response.json()
    if data['result'] != 'success':
        update.message.reply_text('Ошибка при получении данных. Попробуйте позже.')
        return

    rate = data['conversion_rate']
    update.message.reply_text(f'Текущий курс {currency} к {BASE_CURRENCY}: {rate} рублей')




if __name__ == '__main__':
    # Включаем логирование
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    # Парсим переменные окружения
    load_dotenv()
    KEY = os.getenv('KEY')
    TOKEN = os.getenv('TOKEN')

    # Задаем базовую валюту
    BASE_CURRENCY = 'RUB'

    # Логика бота
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("rate", rate))
    updater.start_polling()
    updater.idle()
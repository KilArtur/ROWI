# Создание Телеграм-бота для отслеживания курсов валют
## Описание задачи:
Создать Телеграм-бота, который будет предоставлять актуальную информацию о курсе рубля к основным валютам. Бот должен уметь принимать запросы от пользователей и возвращать курсы валют в реальном времени.
## Функциональные требования:
Команды бота:
- /start: Приветственное сообщение и инструкция по использованию бота.  
- /rate [currency]: возвращает текущий курс указанной валюты по отношению к базовой валюте (RUB).  
## Поддержка валют:
Бот должен поддерживать основные мировые валюты (USD, EUR).
## Источники данных:
Использовать надежный API для получения актуальных курсов валют, в данном случае ExchangeRate-API
## Результат
Telegram bot был перенесен на хостинг [Railway](https://railway.app) для непрерывной работы  
Telegram bot доступен по [ссылке](https://t.me/rowicurrencybot)

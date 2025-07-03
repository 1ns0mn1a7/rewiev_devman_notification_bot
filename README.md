# Devman Review Notification Bot

Этот бот автоматически уведомляет вас в Telegram, когда преподаватель проверяет ваши работы на [dvmn.org](dvmn.org).

## Возможности

- Получение информации о проверке ваших уроков через API Девмана.
- Поддержка Long Polling — бот реагирует мгновенно.
- Отправка сообщений в Telegram с результатом проверки, названием урока и ссылкой на него.

## Установка

1. Установите репозиторий:
```bash
git clone https://github.com/1ns0mn1a7/rewiev_devman_notification_bot
cd rewiev_devman_notification_bot
```
2. Создайте и активируйте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate     # macOS / Linux
venv\Scripts\activate        # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Настройка

Создайте файл `.env` в корне проекта и добавьте в него:
```
DVMN_API_TOKEN=ваш_токен_от_Devman
TELEGRAM_BOT_TOKEN=токен_вашего_Telegram_бота
TELEGRAM_CHAT_ID=ваш_чат_id
```

- `DVMN_API_TOKEN` — можно получить в [Devman.](https://dvmn.org/)

- `TELEGRAM_BOT_TOKEN` — создается через @BotFather в Telegram.

- `TELEGRAM_CHAT_ID` — узнайте у @userinfobot в Telegram.


## Запуск

Активировать бота:
```bash
python notification_bot.py
```

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](dvmn.org).

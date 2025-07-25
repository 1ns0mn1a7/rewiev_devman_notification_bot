import os
import sys
import time
import logging
import requests
from dotenv import load_dotenv
from telegram import Bot


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot: Bot, chat_id: int):
        super().__init__()
        self.tg_bot = tg_bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        try:
            self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)
        except Exception:
            pass


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("dvmn_bot")


def check_for_review_updates(auth_token: str, telegram_bot: Bot, telegram_chat_id: int):
    api_url = "https://dvmn.org/api/long_polling/"
    headers = {"Authorization": f"Token {auth_token}"}
    params = {}

    logger.info("Начинаем отслеживать проверки на DVMN.")
    while True:
        try:
            response = requests.get(api_url, headers=headers, params=params, timeout=60)
            response.raise_for_status()
            review_status = response.json()

            if review_status["status"] == "timeout":
                params["timestamp"] = review_status["timestamp_to_request"]
            elif review_status["status"] == "found":
                params["timestamp"] = review_status["last_attempt_timestamp"]

                for attempt in review_status["new_attempts"]:
                    lesson_title = attempt["lesson_title"]
                    is_negative = attempt["is_negative"]
                    lesson_url = attempt["lesson_url"]

                    if is_negative:
                        result_text = "К сожалению, в работе нашлись ошибки."
                    else:
                        result_text = "Преподавателю всё понравилось, можно приступать к следующему уроку!"

                    message = (
                        f"У вас проверили работу «{lesson_title}»\n\n"
                        f"{result_text}\n"
                        f"Ссылка на урок: {lesson_url}"
                    )

                    telegram_bot.send_message(
                        chat_id=telegram_chat_id,
                        text=message
                    )
                    logger.info(f"Отправлено сообщение о проверке: {lesson_title}")

        except requests.exceptions.ReadTimeout:
            logger.warning("Таймаут запроса")
            time.sleep(5)
            continue
        except requests.exceptions.ConnectionError:
            logger.error("Ошибка соединения.")
            time.sleep(5)


def main():
    load_dotenv()

    devman_token = os.environ["DVMN_API_TOKEN"]
    telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_chat_id = int(os.environ["TELEGRAM_CHAT_ID"])

    telegram_bot = Bot(token=telegram_token)

    telegram_handler = TelegramLogsHandler(telegram_bot, telegram_chat_id)
    telegram_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    telegram_handler.setFormatter(formatter)
    logger.addHandler(telegram_handler)

    telegram_bot.send_message(chat_id=telegram_chat_id, text="Бот запущен.")
    logger.info("Бот запущен.")

    check_for_review_updates(devman_token, telegram_bot, telegram_chat_id)


if __name__ == "__main__":
    main()

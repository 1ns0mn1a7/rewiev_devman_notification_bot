import os
import requests
from dotenv import load_dotenv
from telegram import Bot


def check_for_review_updates(auth_token: str, telegram_bot: Bot, telegram_chat_id: int):
    api_url = "https://dvmn.org/api/long_polling/"
    headers = {"Authorization": f"Token {auth_token}"}
    params = {}
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

        except requests.exceptions.ReadTimeout:
            continue


def main():
    load_dotenv()

    devman_token = os.environ["DVMN_API_TOKEN"]
    telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
    telegram_chat_id = int(os.environ["TELEGRAM_CHAT_ID"])

    telegram_bot = Bot(token=telegram_token)

    check_for_review_updates(devman_token, telegram_bot, telegram_chat_id)


if __name__ == "__main__":
    main()

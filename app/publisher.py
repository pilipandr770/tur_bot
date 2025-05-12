# === app/publisher.py ===
import requests
from flask import current_app
import os

def send_to_telegram(text, image_path=None):
    token = current_app.config['TELEGRAM_TOKEN']
    chat_id = current_app.config['TELEGRAM_CHAT_ID']

    try:
        # Якщо є картинка — спочатку відправляємо її
        if image_path and os.path.exists(image_path):
            with open(image_path, 'rb') as photo:
                photo_response = requests.post(
                    f"https://api.telegram.org/bot{token}/sendPhoto",
                    data={'chat_id': chat_id},
                    files={'photo': photo}
                )
                if photo_response.status_code != 200:
                    print(f"[!] Помилка публікації фото в Telegram: {photo_response.text}")

        # Тепер відправляємо сам текст
        if text:
            text_response = requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data={'chat_id': chat_id, 'text': text[:3500]}
            )
            if text_response.status_code != 200:
                print(f"[!] Помилка публікації тексту в Telegram: {text_response.text}")

    except Exception as e:
        print(f"[!] Виняток при надсиланні в Telegram: {e}")

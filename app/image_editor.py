# === app/image_editor.py ===
import openai
import requests
from flask import current_app
import os

def process_image_from_prompt(article_text, save_path):
    """
    Генерирует промпт на основе текста статьи и создает картинку через DALL·E.
    """
    openai.api_key = current_app.config['OPENAI_API_KEY']
    model = current_app.config.get('DALLE_MODEL', 'dall-e-3')
    prompt = f"Фотореалистичное изображение к статье: {article_text[:300]}... Без людей, надписей, логотипов и рекламы."
    print(f"[LOG] Генерируем промпт для картинки: {prompt}")
    try:
        print("[LOG] Запрос на генерацию изображения через DALL·E...")
        response = openai.images.generate(
            prompt=prompt,
            n=1,
            size="1024x1024",
            model=model
        )
        image_url = response.data[0].url
        image_data = requests.get(image_url).content
        with open(save_path, 'wb') as f:
            f.write(image_data)
        print(f"[LOG] Картинка успешно сгенерирована и сохранена: {save_path}")
        return save_path
    except Exception as e:
        print(f"[!] Ошибка генерации картинки: {e}")
        return None

       
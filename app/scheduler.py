# === app/scheduler.py ===
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from datetime import datetime
from .rss_reader import fetch_articles
from .rewriter import rewrite_text
from .publisher import send_to_telegram
from .models import Article
from . import db
import os
import uuid
from .image_editor import process_image_from_prompt

def start_scheduler(app):
    scheduler = BackgroundScheduler(timezone=pytz.timezone('Europe/Kiev'))

    @scheduler.scheduled_job('interval', minutes=3)
    def job():
        with app.app_context():
            print("🔄 Запуск шедулера: перевірка RSS...")
            fetch_articles()

            now = datetime.now(pytz.timezone('Europe/Kiev'))
            print(f"[LOG] Текущее время: {now}")
            articles = Article.query.filter(
                Article.is_posted == False,
                Article.publish_at != None,
                Article.publish_at <= now
            ).all()
            print(f"[LOG] Найдено статей для публикации: {len(articles)}")
            for article in articles:
                try:
                    # Шаг 1: Генерация текста статьи
                    print(f"[LOG] Генерируем текст для статьи ID {article.id}")
                    rewritten = rewrite_text(article.original_text)
                    article.rewritten_text = rewritten
                    print(f"[LOG] Текст успешно сгенерирован для статьи ID {article.id}")
                    
                    # Шаг 2: Генерация картинки на основе текста
                    print(f"[LOG] Генерируем изображение для статьи ID {article.id}")
                    filename = f"img_{uuid.uuid4().hex}.jpg"
                    image_path = os.path.join("static", "images", filename)
                    image_path = process_image_from_prompt(rewritten, image_path)
                    # Сохраняем путь к изображению в статье
                    article.image_path = image_path
                    print(f"[LOG] Изображение успешно сгенерировано: {image_path}")
                    
                    # Шаг 3: Публикация статьи с изображением
                    send_to_telegram(rewritten, image_path)
                    print(f"[LOG] Статья ID {article.id} отправлена в Telegram")
                    article.is_posted = True
                    db.session.commit()
                    print(f"✅ Опубліковано статтю ID {article.id}")
                except Exception as e:
                    print(f"[!] Помилка обробки статті ID {article.id}: {e}")

    scheduler.start()

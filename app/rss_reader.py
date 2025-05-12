# === app/rss_reader.py ===
import feedparser
from bs4 import BeautifulSoup
import requests
from .models import Article
from . import db
from flask import current_app
from uuid import uuid4
import os
from datetime import datetime
import pytz

def fetch_articles():
    feed_url = current_app.config['RSS_FEED_URL']
    print(f"[LOG] Получаем RSS: {feed_url}")
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        print(f"[LOG] Обработка новости: {entry.get('title', '[без названия]')}")
        content = extract_full_text(entry)
        if not content:
            print("[LOG] Пропуск: нет контента")
            continue
        if Article.query.filter_by(original_text=content).first():
            print("[LOG] Пропуск: статья уже есть в базе")
            continue        # Изображение будет генерироваться позже на основе текста
        new_article = Article(
            original_text=content,
            source_name=entry.get("source", {}).get("title", ""),
            image_path=None,  # Изображение добавится при публикации
            publish_at=datetime.now(pytz.timezone('Europe/Kiev'))
        )
        db.session.add(new_article)
        print(f"[LOG] Новая статья добавлена в базу: {new_article}")
    db.session.commit()
    print("[LOG] Все новые статьи сохранены в базе.")

def extract_full_text(entry):
    if 'content' in entry:
        return BeautifulSoup(entry.content[0].value, 'html.parser').get_text()
    elif 'summary' in entry:
        return BeautifulSoup(entry.summary, 'html.parser').get_text()
    return ""

# Функция get_image_url больше не используется, т.к. изображения генерируются на основе текста
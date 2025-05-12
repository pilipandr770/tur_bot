from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()  # Добавлено для поддержки миграций

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)
    migrate.init_app(app, db)  # Инициализация Flask-Migrate

    from . import models
    with app.app_context():
        db.create_all()

    return app

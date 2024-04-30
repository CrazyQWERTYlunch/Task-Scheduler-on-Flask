"""Настройки конфигурации приложения."""

class Config:
    """Базовая конфигурация приложения."""
    
    SECRET_KEY = 'my_secret_key'  # Секретный ключ для защиты сессий и форм
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'  # Путь к базе данных SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключает отслеживание изменений объектов и сигналы SQLAlchemy

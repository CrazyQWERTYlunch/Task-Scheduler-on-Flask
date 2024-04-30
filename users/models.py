"""Модели данных для приложения users."""

from flask_login import UserMixin
from sqlalchemy import JSON
from database import db

class User(UserMixin, db.Model):
    """
    Модель пользователя.

    :param id: Уникальный идентификатор пользователя.
    :type id: int
    :param email: Адрес электронной почты пользователя.
    :type email: str
    :param username: Имя пользователя.
    :type username: str
    :param password: Хэш пароля пользователя.
    :type password: str
    :param notification_settings: Настройки уведомлений пользователя.
    :type notification_settings: dict
    :param todo_lists: Связь с списками задач пользователя.
    :type todo_lists: list[TodoList]
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(1000), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    notification_settings = db.Column(JSON, nullable=False, default={})
    todo_lists = db.relationship('TodoList', backref='user', lazy=True)

class UserStats(db.Model):
    """
    Модель статистики пользователя.

    :param id: Уникальный идентификатор записи статистики.
    :type id: int
    :param user_id: Идентификатор пользователя.
    :type user_id: int
    :param total_todo: Общее количество списков задач пользователя.
    :type total_todo: int
    :param total_tasks: Общее количество задач пользователя.
    :type total_tasks: int
    :param active_tasks: Количество активных задач пользователя.
    :type active_tasks: int
    :param completed_tasks: Количество завершенных задач пользователя.
    :type completed_tasks: int
    :param incomplete_tasks: Количество незавершенных задач пользователя.
    :type incomplete_tasks: int
    :param completion_percentage: Процент завершения задач пользователя.
    :type completion_percentage: float
    :param user: Связь с пользователем.
    :type user: User
    """
    __tablename__ = 'user_stats'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_todo = db.Column(db.Integer, default=0)
    total_tasks = db.Column(db.Integer, default=0)
    active_tasks = db.Column(db.Integer, default=0)
    completed_tasks = db.Column(db.Integer, default=0)  
    incomplete_tasks = db.Column(db.Integer, default=0)  
    completion_percentage = db.Column(db.Float, default=0.0)
    user = db.relationship('User', backref='stats', lazy=True)

    def __repr__(self):
        """
        Представление объекта UserStats в виде строки.

        :return: Строковое представление объекта UserStats.
        :rtype: str
        """
        return f"UserStats('{self.user_id}', '{self.total_tasks}', '{self.completed_tasks}', '{self.incomplete_tasks}', '{self.completion_percentage}')"

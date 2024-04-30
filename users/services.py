"""Сервисы для работы с пользователями и статистикой."""

from datetime import datetime
from sqlalchemy import func, case
from .models import User, UserStats
from todo_list.models import Task, TodoList
from database import db

class UserService:
    """
    Сервис пользователей.

    Предоставляет методы для работы с пользователями.
    """

    @staticmethod
    def get_user_by_id(user_id):
        """
        Получить пользователя по его идентификатору.

        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :return: Объект пользователя или None, если пользователь не найден.
        :rtype: User or None
        """
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_user(username:str):
        """
        Получить пользователя по его имени пользователя.

        :param username: Имя пользователя.
        :type username: str
        :return: Объект пользователя или None, если пользователь не найден.
        :rtype: User or None
        """
        user =  User.query.filter_by(username=username).first()
        return user

    @staticmethod
    def register_user(email:str, username: str, password: str):
        """
        Зарегистрировать нового пользователя.

        :param email: Адрес электронной почты нового пользователя.
        :type email: str
        :param username: Имя нового пользователя.
        :type username: str
        :param password: Пароль нового пользователя.
        :type password: str
        """
        new_user = User(email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def authenticate_user(username: str, password: str):
        """
        Аутентификация пользователя.

        :param username: Имя пользователя.
        :type username: str
        :param password: Пароль пользователя.
        :type password: str
        :return: Объект пользователя или None, если пользователь не найден или пароль неверный.
        :rtype: User or None
        """
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            return user
        return None

    @staticmethod
    def password_update(password, user_id):
        """
        Обновить пароль пользователя.

        :param password: Новый пароль пользователя.
        :type password: str
        :param user_id: Идентификатор пользователя.
        :type user_id: int
        """
        user = UserService.get_user_by_id(user_id)
        user.password = password
        db.session.commit()

    @staticmethod
    def get_user_stats(user_id):
        """
        Получить статистику пользователя.

        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :return: Объект статистики пользователя или None, если статистика не найдена.
        :rtype: UserStats or None
        """
        user = UserStats.query.filter_by(user_id=user_id).first()
        return user

    @staticmethod
    def user_stats_create(user_id, total_todo, total_tasks, completed_tasks,
                           active_tasks ,incomplete_tasks, completion_percentage):
        """
        Создать статистику пользователя.

        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :param total_todo: Общее количество списков задач пользователя.
        :type total_todo: int
        :param total_tasks: Общее количество задач пользователя.
        :type total_tasks: int
        :param completed_tasks: Количество завершенных задач пользователя.
        :type completed_tasks: int
        :param active_tasks: Количество активных задач пользователя.
        :type active_tasks: int
        :param incomplete_tasks: Количество незавершенных задач пользователя.
        :type incomplete_tasks: int
        :param completion_percentage: Процент завершения задач пользователя.
        :type completion_percentage: float
        :return: Объект статистики пользователя.
        :rtype: UserStats
        """
        user_stats= UserStats(user_id=user_id,
                            total_todo=total_todo,
                            total_tasks=total_tasks,
                            active_tasks=active_tasks,
                            completed_tasks=completed_tasks,
                            incomplete_tasks=incomplete_tasks,
                            completion_percentage=completion_percentage)
        db.session.add(user_stats)
        db.session.commit()
        return user_stats

    @staticmethod
    def user_stats_update(user_id, total_todo, total_tasks, completed_tasks,
                           active_tasks ,incomplete_tasks, completion_percentage):
        """
        Обновить статистику пользователя.

        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :param total_todo: Общее количество списков задач пользователя.
        :type total_todo: int
        :param total_tasks: Общее количество задач пользователя.
        :type total_tasks: int
        :param completed_tasks: Количество завершенных задач пользователя.
        :type completed_tasks: int
        :param active_tasks: Количество активных задач пользователя.
        :type active_tasks: int
        :param incomplete_tasks: Количество незавершенных задач пользователя.
        :type incomplete_tasks: int
        :param completion_percentage: Процент завершения задач пользователя.
        :type completion_percentage: float
        :return: Объект статистики пользователя.
        :rtype: UserStats
        """
        user_stats = UserService.get_user_stats(user_id)
        user_stats.total_todo = total_todo
        user_stats.total_tasks = total_tasks
        user_stats.active_tasks = active_tasks
        user_stats.completed_tasks = completed_tasks
        user_stats.incomplete_tasks = incomplete_tasks
        user_stats.completion_percentage = completion_percentage
        db.session.commit()
        return user_stats

class StatisticService:
    """
    Сервис статистики.

    Предоставляет методы для работы со статистикой пользователей.
    """

    @staticmethod
    def get_user_total_todo_lists(user_id):
        """
        Получить общее количество списков задач пользователя.

        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :return: Общее количество списков задач пользователя.
        :rtype: int
        """
        return TodoList.query.filter(TodoList.user_id == user_id).count()

    @staticmethod
    def get_user_total_tasks(user_id):
        """
        Получить общее количество задач пользователя.

        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :return: Общее количество задач пользователя.
        :rtype: int
        """
        tasks = Task.query.join(TodoList).filter(TodoList.user_id == user_id).count()
        return tasks

    @staticmethod
    def get_user_active_tasks(user_id):
        """
        Получить количество активных задач пользователя.

        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :return: Количество активных задач пользователя.
        :rtype: int
        """
        tasks = Task.query.join(TodoList).filter(
            TodoList.user_id == user_id,
            Task.is_complete == False,
            Task.deadline_date > datetime.now()).count()
        return tasks

    @staticmethod
    def get_user_completed_tasks(user_id):
        """
        Получить количество завершенных задач пользователя.

        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :return: Количество завершенных задач пользователя.
        :rtype: int
        """
        tasks = Task.query.join(TodoList).filter(TodoList.user_id == user_id, Task.is_complete == True).count()
        return tasks

    @staticmethod
    def get_user_incompleted_tasks(user_id):
        """
        Получить количество незавершенных задач пользователя.

        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :return: Количество незавершенных задач пользователя.
        :rtype: int
        """
        tasks = Task.query.join(TodoList).filter(
            TodoList.user_id == user_id,
            Task.is_complete == False,
            Task.deadline_date < datetime.now()).count()
        return tasks

    @staticmethod
    def calculate_completion_percentage(user_id):
        """
        Рассчитать процент завершения задач пользователя.

        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :return: Процент завершения задач пользователя.
        :rtype: float
        """
        completion_percentage = db.session.query(
            func.round(func.avg(func.cast(Task.is_complete, db.Integer)) * 100, 2)
        ).join(TodoList).filter(
            TodoList.user_id == user_id
        ).scalar()

        return completion_percentage or 0
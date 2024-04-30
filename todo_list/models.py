"""Модели данных для приложения todo_list."""

from datetime import datetime
from sqlalchemy import DateTime, event
from database import db

class Task(db.Model):
    """
    Модель задачи.

    :param id: Идентификатор задачи.
    :type id: int
    :param title: Заголовок задачи.
    :type title: str
    :param description: Описание задачи.
    :type description: str
    :param is_complete: Флаг завершенности задачи.
    :type is_complete: bool
    :param created_at: Дата и время создания задачи.
    :type created_at: datetime
    :param deadline_date: Дата и время крайнего срока выполнения задачи.
    :type deadline_date: datetime, optional
    :param completed_at: Дата и время завершения задачи.
    :type completed_at: datetime, optional
    :param todo_id: Идентификатор списка задач, к которому принадлежит задача.
    :type todo_id: int
    """
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(250), nullable=True)
    is_complete = db.Column(db.Boolean, default=False)
    created_at = db.Column(DateTime(timezone=True), default=datetime.now)
    deadline_date = db.Column(DateTime(timezone=True), nullable=True)
    completed_at = db.Column(DateTime(timezone=True), nullable=True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo_list.id'), nullable=False)

@event.listens_for(Task, 'before_update')
def update_timestamp(mapper, connection, target):
    """
    Обновляет временную метку при завершении задачи.

    :param mapper: Mapper.
    :type mapper: Mapper
    :param connection: Соединение с базой данных.
    :type connection: Connection
    :param target: Экземпляр задачи.
    :type target: Task
    """
    if target.is_complete and not target.completed_at:
        target.completed_at = datetime.now()
    else:
        target.completed_at = None

class TodoList(db.Model):
    """
    Модель списка задач.

    :param id: Идентификатор списка задач.
    :type id: int
    :param title: Заголовок списка задач.
    :type title: str
    :param user_id: Идентификатор пользователя, которому принадлежит список задач.
    :type user_id: int
    :param tasks: Список задач, принадлежащих данному списку задач.
    :type tasks: RelationshipProperty
    """
    __tablename__ = 'todo_list'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Task', backref='todo_list', lazy=True, cascade='all, delete-orphan')
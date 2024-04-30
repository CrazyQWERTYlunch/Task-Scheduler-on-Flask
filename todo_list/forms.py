"""Формы для приложения todo_list."""

from datetime import datetime
from pydantic import BaseModel
from typing import List, Union

class TodoCreateForm(BaseModel):
    """
    Форма создания нового списка задач.

    :param title: Заголовок списка задач.
    :type title: str
    """
    title: str

class TodoListForm(TodoCreateForm):
    """
    Форма списка задач.

    :param id: Идентификатор списка задач.
    :type id: int
    :param tasks: Список задач в рамках списка задач.
    :type tasks: List[Union["Task", None]]
    """
    id: int
    tasks: List[Union["Task", None]] = []

class TaskBaseForm(BaseModel):
    """
    Базовая форма для задачи.

    :param title: Заголовок задачи.
    :type title: str
    :param description: Описание задачи.
    :type description: str, optional
    """
    title: str
    description: str = None

class TaskForm(TaskBaseForm):
    """
    Форма задачи.

    :param id: Идентификатор задачи.
    :type id: int
    :param is_complete: Флаг завершенности задачи.
    :type is_complete: bool
    :param todo_list_id: Идентификатор списка задач, к которому принадлежит задача.
    :type todo_list_id: int
    """
    id: int
    is_complete: bool
    todo_list_id: int

class TaskUpdateForm(TaskBaseForm):
    """
    Форма обновления задачи.

    :param id: Идентификатор задачи.
    :type id: int
    """
    id: int

class TaskCreateForm(TaskBaseForm):
    """
    Форма создания новой задачи.

    :param deadline_date: Дата и время крайнего срока выполнения задачи.
    :type deadline_date: datetime, optional
    :param todo_id: Идентификатор списка задач, к которому принадлежит задача.
    :type todo_id: int
    """
    deadline_date: datetime = None
    todo_id: int
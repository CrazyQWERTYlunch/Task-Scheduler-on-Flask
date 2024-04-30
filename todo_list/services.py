"""Сервисы для работы с данными приложения todo_list."""
from todo_list.models import TodoList, Task
from database import db

class TodoService:
    """
    Сервис для работы с списками задач.

    """
    @staticmethod
    def create_todo(title, user_id):
        """
        Создает новый список задач.

        :param title: Заголовок списка задач.
        :type title: str
        :param user_id: Идентификатор пользователя, которому принадлежит список задач.
        :type user_id: int
        """
        new_todo = TodoList(title=title, user_id=user_id)
        db.session.add(new_todo)
        db.session.commit()

    @staticmethod
    def get_todo(todo_id):
        """
        Возвращает список задач по его идентификатору.

        :param todo_id: Идентификатор списка задач.
        :type todo_id: int
        :return: Список задач.
        :rtype: TodoList
        """
        return TodoList.query.get_or_404(todo_id)
    
    @staticmethod
    def get_all_todo(user_id):
        """
        Возвращает все списки задач для указанного пользователя.

        :param user_id: Идентификатор пользователя.
        :type user_id: int
        :return: Список всех списков задач пользователя.
        :rtype: list[TodoList]
        """
        return TodoList.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def update_todo(todo_id, title):
        """
        Обновляет заголовок списка задач.

        :param todo_id: Идентификатор списка задач.
        :type todo_id: int
        :param title: Новый заголовок списка задач.
        :type title: str
        """
        todo_list = TodoList.query.filter_by(id=todo_id).first()
        todo_list.title = title 
        db.session.commit()

    @staticmethod
    def delete_todo(todo_id):
        """
        Удаляет список задач.

        :param todo_id: Идентификатор списка задач.
        :type todo_id: int
        """
        todo = TodoList.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()       

    @staticmethod
    def count_tasks(todo_id):
        """
        Возвращает количество задач в списке, количество активных задач и количество завершенных задач.

        :param todo_id: Идентификатор списка задач.
        :type todo_id: int
        :return: Количество всех задач, активных задач и завершенных задач в списке.
        :rtype: tuple[int, int, int]
        """
        all_tasks = Task.query.filter_by(todo_id=todo_id).count()
        active_tasks = Task.query.filter_by(todo_id=todo_id, is_complete=False).count()
        completed_tasks = Task.query.filter_by(todo_id=todo_id, is_complete=True).count()
        return all_tasks, active_tasks, completed_tasks
    
    @staticmethod
    def get_tasks_from_todo_list(todo_id):
        """
        Возвращает все задачи из списка задач.

        :param todo_id: Идентификатор списка задач.
        :type todo_id: int
        :return: Список всех задач в указанном списке задач.
        :rtype: list[Task]
        """
        tasks = Task.query.filter_by(todo_list_id=todo_id).all()
        return tasks

    
class TaskService:
    """
    Сервис для работы с задачами.
    """
    @staticmethod
    def get_task(task_id):
        """
        Возвращает задачу по ее идентификатору.

        :param task_id: Идентификатор задачи.
        :type task_id: int
        :return: Задача.
        :rtype: Task
        """
        return Task.query.get_or_404(task_id)
    
    @staticmethod
    def add_task(title, description, deadline_date, todo_id):
        """
        Добавляет новую задачу в список задач.

        :param title: Заголовок задачи.
        :type title: str
        :param description: Описание задачи.
        :type description: str
        :param deadline_date: Дата и время крайнего срока выполнения задачи.
        :type deadline_date: datetime
        :param todo_id: Идентификатор списка задач, к которому принадлежит задача.
        :type todo_id: int
        """
        new_task = Task(title=title,
                        description=description,
                        deadline_date=deadline_date,
                        todo_id=todo_id)
        db.session.add(new_task)
        db.session.commit()

    @staticmethod
    def complete_task(task_id):
        """
        Помечает задачу как завершенную или отменяет это действие, если она уже завершена.

        :param task_id: Идентификатор задачи.
        :type task_id: int
        """
        task = TaskService.get_task(task_id)
        task.is_complete = not task.is_complete 
        db.session.commit()

    @staticmethod
    def update_task(id, title, description):
        """
        Обновляет информацию о задаче.

        :param id: Идентификатор задачи.
        :type id: int
        :param title: Новый заголовок задачи.
        :type title: str
        :param description: Новое описание задачи.
        :type description: str
        """
        task = TaskService.get_task(id)
        task.title = title
        task.description = description
        db.session.commit()

    @staticmethod
    def delete_task(task_id):
        """
        Удаляет задачу.

        :param task_id: Идентификатор задачи.
        :type task_id: int
        """
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
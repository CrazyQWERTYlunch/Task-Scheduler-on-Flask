"""
Модуль содержит тесты для проверки функциональности приложения управления задачами.

TestFixtures:
    - app: Фикстура для создания экземпляра приложения.
    - client: Фикстура для создания клиента.
    - authenticated_client: Фикстура для создания авторизованного клиента.
    - create_tasks_and_todo: Фикстура для создания тестовых задач и списков дел.

Test Functions:
    - test_todo_list_index_authenticated: Тест просмотра списка дел авторизованным пользователем.
    - test_todo_add: Тест добавления нового списка дел.
    - test_todo_update: Тест обновления списка задач.
    - test_todo_delete: Тест удаления списка задач.
    - test_task_add: Тест добавления задачи в список дел.
    - test_task_complete: Тест выполнения задачи.
    - test_task_update: Тест обновления задачи.
    - test_task_delete: Тест удаления задачи.
"""
import os
import sys
import pytest
from datetime import datetime
from flask_login import login_user
from werkzeug.datastructures import MultiDict
# Добавляем путь к модулям приложения
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Импортируем необходимые модули
from app import create_app
from database import db
from users.models import User
from users.services import UserService
from todo_list.models import TodoList, Task
from todo_list.services import TodoService, TaskService


@pytest.fixture
def app():
    """
    Фикстура для создания экземпляра приложения.

    Returns:
        Flask app: Экземпляр приложения Flask.

    """
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Фикстура для создания клиента.

    Args:
        app: Экземпляр приложения Flask.

    Returns:
        Flask test client: Тестовый клиент Flask.

    """
    return app.test_client()


@pytest.fixture
def authenticated_client(client, app):
    """
    Фикстура для создания авторизованного клиента.

    Args:
        client: Тестовый клиент Flask.
        app: Экземпляр приложения Flask.

    Returns:
        Flask test client: Аутентифицированный тестовый клиент Flask.

    """
    user_data = {'email': 'test@example.com', 'username': 'test_user', 'password': 'password'}
    UserService.register_user(**user_data)
    
    with app.test_request_context():
        user = User.query.filter_by(username='test_user').first()
        login_user(user)
    
    return client


@pytest.fixture
def create_tasks_and_todo(app):
    """
    Фикстура для создания тестовых задач и списков дел.

    Args:
        app: Экземпляр приложения Flask.

    Returns:
        dict: Словарь с ID созданных списков задач и задач.

    """
    with app.app_context():
        TodoService.create_todo(title='Test Todo List 1', user_id=1)
        TodoService.create_todo(title='Test Todo List 2', user_id=1)
        TaskService.add_task(title='Test Task',
                            description='Test Description',
                            deadline_date=datetime(2023, 12, 20),
                            todo_id=2)
        TaskService.add_task(title='Test Task_2',
                            description='Test Description_2',
                            deadline_date=datetime(2023, 12, 21),
                            todo_id=2)
   
    return {'todo_list_ids': [1, 2], 'task_ids': [1, 2]}


def test_todo_list_index_authenticated(authenticated_client):
    """
    Тест для проверки просмотра списка дел авторизованным пользователем.

    Args:
        authenticated_client: Аутентифицированный тестовый клиент Flask.

    """
    TodoService.create_todo(title='Test Todo List', user_id=1)

    response = authenticated_client.get('/todo_list', follow_redirects=True)
   
    assert response.status_code == 200  # Ожидаем успешный ответ
    assert 'Test Todo List' in response.data.decode('utf-8')


def test_todo_add(authenticated_client):
    """
    Тест для проверки добавления нового списка дел.

    Args:
        authenticated_client: Аутентифицированный тестовый клиент Flask.

    """
    form_data = MultiDict({'title': 'Test Todo List'})
   
    response = authenticated_client.post('/todo_list/add', data=form_data)
    
    assert response.status_code == 302 
    assert response.location == '/todo_list/'  
    assert TodoService.get_todo(todo_id=1) is not None


def test_todo_update(authenticated_client):
    """
    Тест для проверки обновления списка задач.

    Args:
        authenticated_client: Аутентифицированный тестовый клиент Flask.

    """
    TodoService.create_todo(title='Test Todo List', user_id=1)
    form_data = MultiDict({'title': 'Updated Todo List'})
    
    response = authenticated_client.post('/todo_list/update/1', data=form_data)
    
    assert response.status_code == 302  
    assert response.location == '/todo_list/'

    updated_todo_list = TodoList.query.filter_by(title='Updated Todo List').first()
    assert updated_todo_list is not None


def test_todo_delete(authenticated_client):
    """
    Тест для проверки удаления списка задач.

    Args:
        authenticated_client: Аутентифицированный тестовый клиент Flask.

    """
    TodoService.create_todo(title='Test Todo List', user_id=1)
    
    response = authenticated_client.post('/todo_list/delete/1')
    
    assert response.status_code == 302 
    assert response.location == '/todo_list/'

    deleted_todo_list = TodoList.query.filter_by(title='Test Todo List').first()
    assert deleted_todo_list is None


def test_task_add(app, authenticated_client):
    """
    Тест добавления задачи в список дел.

    Args:
        app: Экземпляр приложения Flask.
        client: Тестовый клиент Flask.
        authenticated_client: Аутентифицированный тестовый клиент Flask.

    """
    with app.app_context():
        TodoService.create_todo(title='Test Todo List 1', user_id=1)
        TodoService.create_todo(title='Test Todo List 2', user_id=1)

    form_data = MultiDict({
        'title': 'Test Task 2',
        'description': 'Test Description 2',
        'deadline_date': datetime(2023, 12, 20)
    })

    with app.app_context():
        response = authenticated_client.post('/todo_list/2/task-add', data=form_data)

    assert response.status_code == 302
    assert response.location == '/todo_list/2'

    with app.app_context():
        created_task = Task.query.filter_by(title='Test Task 2').first()
        assert created_task is not None


def test_task_complete(app, authenticated_client, create_tasks_and_todo):
    """
    Тест завершения задачи.

    Args:
        app: Экземпляр приложения Flask.
        authenticated_client: Аутентифицированный тестовый клиент Flask.
        create_tasks_and_todo: Фикстура для создания тестовых задач и списков дел.

    """
    todo_list_ids = create_tasks_and_todo['todo_list_ids']
    task_ids = create_tasks_and_todo['task_ids']

    with app.app_context():
        response = authenticated_client.post(
            f'/todo_list/{todo_list_ids[1]}/task-completed',
            data={'task_id': task_ids[0]}
        )

    assert response.status_code == 302
    assert response.location == '/todo_list/2'

    with app.app_context():
        completed_task = Task.query.filter_by(id=task_ids[0]).first()
        uncompleted_task = Task.query.filter_by(id=task_ids[1]).first()
        assert completed_task.is_complete
        assert not uncompleted_task.is_complete


def test_task_update(app, authenticated_client, create_tasks_and_todo):
    """
    Тест обновления задачи.

    Args:
        app: Экземпляр приложения Flask.
        authenticated_client: Аутентифицированный тестовый клиент Flask.
        create_tasks_and_todo: Фикстура для создания тестовых задач и списков дел.

    """
    todo_list_ids = create_tasks_and_todo['todo_list_ids']
    task_ids = create_tasks_and_todo['task_ids']

    form_data = {
        'title': 'Updated Task',
        'description': 'Updated Description',
        'id': task_ids[0]
    }

    with app.app_context():
        response = authenticated_client.post(
            f'/todo_list/{todo_list_ids[1]}/task-update',
            data=form_data
        )

    assert response.status_code == 302
    assert response.location == f'/todo_list/{todo_list_ids[1]}'

    with app.app_context():
        updated_task = Task.query.filter_by(id=task_ids[0]).first()
        assert updated_task.title == 'Updated Task'
        assert updated_task.description == 'Updated Description'


def test_task_delete(app, authenticated_client, create_tasks_and_todo):
    """
    Тест удаления задачи.

    Args:
        app: Экземпляр приложения Flask.
        authenticated_client: Аутентифицированный тестовый клиент Flask.
        create_tasks_and_todo: Фикстура для создания тестовых задач и списков дел.

    """
    task_ids = create_tasks_and_todo['task_ids']
    todo_list_ids = create_tasks_and_todo['todo_list_ids']

    with app.app_context():
        response = authenticated_client.post(
            f'/todo_list/{todo_list_ids[1]}/task-delete',
            data={'task_id': task_ids[0]}
        )

    assert response.status_code == 302
    assert response.location == f'/todo_list/{todo_list_ids[1]}'

    with app.app_context():
        deleted_task = Task.query.filter_by(id=task_ids[0]).first()
        assert deleted_task is None
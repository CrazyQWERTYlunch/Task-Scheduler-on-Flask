"""
Модуль содержит тесты для проверки функциональности авторизации пользователей.

TestFixtures:
    - app: Фикстура для создания экземпляра приложения Flask.
    - client: Фикстура для создания тестового клиента Flask.

Test Functions:
    - test_register_user: Тест регистрации пользователя.
    - test_login_function: Тест функции входа пользователя.
    - test_logout_function: Тест функции выхода пользователя.
"""
import os
import sys
import pytest

from flask import request
from flask_login import login_user, current_user

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import db
from app import create_app
from users.services import UserService
from auth.routes import login, logout
from users.models import User


@pytest.fixture
def app():
    """
    Фикстура для создания приложения Flask.

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
    Фикстура для создания тестового клиента Flask.

    Args:
        app: Экземпляр приложения Flask.

    Returns:
        Flask test client: Тестовый клиент Flask.

    """
    return app.test_client()


def test_register_user(client, app):
    """
    Тест регистрации пользователя.

    Args:
        client: Тестовый клиент Flask.
        app: Экземпляр приложения Flask.

    """
    user_info = {'email': 'test@example.com', 'username': 'test_user', 'password': 'password'}

    response = client.post('/register', data=user_info, follow_redirects=True)

    assert response.status_code == 200

    user = User.query.filter_by(username='test_user').first()
    assert user is not None

    assert user.email == 'test@example.com'


def test_login_function(client, app):
    """
    Тест функции входа пользователя.

    Args:
        client: Тестовый клиент Flask.
        app: Экземпляр приложения Flask.

    """
    user_info = {'email': 'test@example.com', 'username': 'test_user', 'password': 'password'}
    UserService.register_user(**user_info)

    with app.test_request_context('/login', method='POST', data={'username': 'test_user', 'password': 'wrong_password'}):
        response = login()
        assert response.status_code == 302
        assert response.location == '/login'

    with app.test_request_context('/login', method='POST', data={'username': 'test_user', 'password': 'password'}):
        response = login()
        assert response.status_code == 302
        login_user(User.query.filter_by(username='test_user').first())

    response = client.get('/todo_list')
    assert response.status_code == 308
    assert response.location == 'http://localhost/todo_list/'


def test_logout_function(client, app):
    """
    Тест функции выхода пользователя.

    Args:
        client: Тестовый клиент Flask.
        app: Экземпляр приложения Flask.

    """
    user_info = {'email': 'test@example.com', 'username': 'test_user', 'password': 'password'}
    UserService.register_user(**user_info)

    with app.test_request_context():
        login_user(User.query.filter_by(username='test_user').first())

        response = logout()

        assert response.status_code == 302
        assert request.path == '/'

        assert current_user.is_authenticated is False
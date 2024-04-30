import os
import sys
import pytest
from flask_login import login_user

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database import db
from users.models import User


@pytest.fixture
def app():
    """
    Фикстура для создания экземпляра приложения Flask.

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


@pytest.fixture
def authenticated_client(client, app):
    """
    Фикстура для создания аутентифицированного тестового клиента Flask.

    Args:
        client: Тестовый клиент Flask.
        app: Экземпляр приложения Flask.

    Returns:
        Flask test client: Аутентифицированный тестовый клиент Flask.

    """
    with client.session_transaction() as session:
        user = User(email='test@example.com', username='test_user', password='password123')
        db.session.add(user)
        db.session.commit()
        with app.test_request_context():
            user = User.query.filter_by(username='test_user').first()
            login_user(user)
        
        return client

def test_profile_authenticated(authenticated_client):
    """
    Тест для проверки профиля аутентифицированного пользователя.

    Args:
        authenticated_client: Аутентифицированный тестовый клиент Flask.

    """
    response = authenticated_client.get('/profile', follow_redirects=True)
    assert response.status_code == 200
    response_data = response.get_data(as_text=True)
    assert 'test@example.com' in response_data
    assert 'test_user' in response_data

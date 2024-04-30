"""Основной файл приложения."""
from flask import Flask
from database import db
from config import Config
from users import login_manager
from users.routes import user_blueprint
from todo_list.routes import todo_list_bp
from auth.routes import auth_blueprint


def create_app():
    """Создает и настраивает экземпляр приложения."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)

    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app

def register_blueprints(app):
    """Регистрирует blueprint-ы в приложении."""
    app.register_blueprint(user_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(todo_list_bp)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
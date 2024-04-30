"""Маршруты для аутентификации."""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from users.utils import verify_password, hash_password
from users.services import UserService
from .forms import RegistrationForm

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Обработчик маршрута для входа в систему.

    Если пользователь уже аутентифицирован, перенаправляет на главную страницу.
    Если метод запроса - POST, пытается аутентифицировать пользователя.
    """
    if current_user.is_authenticated:
        return redirect(url_for('todo_list.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = UserService.get_user(username=username)
        if not user or not verify_password(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        return redirect(url_for('todo_list.index'))
    
    return render_template('auth/login.html')

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """
    Обработчик маршрута для регистрации нового пользователя.

    Если пользователь уже аутентифицирован, перенаправляет на главную страницу.
    Если метод запроса - POST, пытается зарегистрировать нового пользователя.
    """
    if current_user.is_authenticated:
        return redirect(url_for('todo_list.index'))

    if request.method == 'POST':
        user_form = RegistrationForm(**request.form)
        if UserService.get_user(username=user_form.username):
            flash('This username already exists', 'error')
            return redirect(url_for('auth.register'))
        
        if user_form.model_validate(user_form):
            user_form.password = hash_password(user_form.password)
            UserService.register_user(**user_form.model_dump())
            flash('You have successfully signed up!', 'success')
            return redirect(url_for('auth.login'))
        flash('Check the input parameters', 'error')

    return render_template('auth/register.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    """
    Обработчик маршрута для выхода пользователя из системы.

    Перенаправляет на страницу входа после выхода.
    """
    logout_user()
    return redirect(url_for('auth.login'))
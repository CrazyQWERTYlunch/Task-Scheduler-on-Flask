"""Маршруты для пользовательского профиля."""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from users import login_manager
from users.utils import hash_password, verify_password
from users.services import UserService, StatisticService
from users.forms import ChangePasswordForm

user_blueprint = Blueprint('user', __name__, url_prefix='/profile')

@user_blueprint.route('/')
@login_required
def profile():
    """
    Обработчик маршрута для отображения профиля пользователя.

    :return: Шаблон профиля пользователя.
    :rtype: flask.Response
    """
    collect_statistics_data(current_user.id)
    user_stats = UserService.get_user_stats(current_user.id)
    return render_template('users/profile.html', user_stats=user_stats)

@login_manager.user_loader
def load_user(user_id):
    """
    Функция для загрузки пользователя.

    :param user_id: Идентификатор пользователя.
    :type user_id: int
    :return: Пользовательский объект.
    :rtype: User
    """
    return UserService.get_user_by_id(user_id)

@user_blueprint.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """
    Обработчик маршрута для изменения пароля пользователя.

    :return: Редирект на страницу профиля.
    :rtype: flask.Response
    """
    form_data = request.form
    form = ChangePasswordForm(**form_data)
    
    if form.model_validate(form):
        current_password = form.current_password
        new_password = form.new_password
        confirm_password = form.confirm_password
        if verify_password(current_user.password, current_password):
            if new_password == confirm_password:
                UserService.password_update(hash_password(new_password), current_user.id)
                flash('Your password has been updated successfully!', 'success')
                return redirect(url_for('user.profile'))
            else:
                flash('New password and confirm password do not match!', 'error')
        else:
            flash('Current password is incorrect!', 'error')
    else:
        flash('Invalid form data!', 'error')

    return redirect(url_for('user.change_password'))

def collect_statistics_data(user_id):
    """
    Сбор статистических данных пользователя.

    :param user_id: Идентификатор пользователя.
    :type user_id: int
    """
    total_todo = StatisticService.get_user_total_todo_lists(current_user.id)
    total_tasks = StatisticService.get_user_total_tasks(current_user.id)
    completed_tasks = StatisticService.get_user_completed_tasks(current_user.id)
    active_tasks = StatisticService.get_user_active_tasks(current_user.id)
    incomplete_tasks = StatisticService.get_user_incompleted_tasks(current_user.id)
    completion_percentage = StatisticService.calculate_completion_percentage(current_user.id)

    user_stats = UserService.get_user_stats(user_id)
    if user_stats:
        UserService.user_stats_update(
            current_user.id, total_todo, total_tasks, 
            completed_tasks, active_tasks, incomplete_tasks,
            completion_percentage
            )
    else:
        UserService.user_stats_create(
            user_id=user_id,
            total_todo=total_todo,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            active_tasks=active_tasks,
            incomplete_tasks=incomplete_tasks,
            completion_percentage=completion_percentage
        )
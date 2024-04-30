"""Маршруты для приложения todo_list."""

from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import current_user, login_required
from todo_list.services import TaskService, TodoService
from todo_list.forms import TaskCreateForm, TaskUpdateForm, TodoCreateForm

todo_list_bp = Blueprint('todo_list', __name__, url_prefix='/todo_list')


@todo_list_bp.errorhandler(404)
def page_not_found(e):
    """
    Обработчик ошибки 404 (страница не найдена).

    :param e: Исключение.
    :type e: Exception
    """
    flash('Страница не найдена.', 'error')
    return redirect(url_for('todo_list.index'))


@todo_list_bp.errorhandler(403)
def forbidden(e):
    """
    Обработчик ошибки 403 (доступ запрещен).

    :param e: Исключение.
    :type e: Exception
    """
    flash('Доступ запрещен.', 'error')
    return redirect(url_for('todo_list.index'))


@todo_list_bp.get('/')
@login_required
def index():
    """
    Отображает список всех списков задач.

    :return: HTML-страница со списками задач.
    :rtype: flask.Response
    """
    todo_lists = TodoService.get_all_todo(current_user.id)
    return render_template('todo_list/index.html', todo_lists=todo_lists, title='Ваши списки задач')


@todo_list_bp.route('/add', methods=['POST'])
def todo_add():
    """
    Добавляет новый список задач.

    :return: HTML-страница с обновленным списком задач или форма для создания нового списка.
    :rtype: flask.Response
    """
    form_data = request.form
    form = TodoCreateForm(**form_data)
    if form.model_validate(form):
        TodoService.create_todo(**form.model_dump(), user_id=current_user.id)
        return redirect(url_for('todo_list.index'))
    return render_template('todo_list.index.html')


@todo_list_bp.route('/update/<int:todo_id>', methods=['POST'])
def todo_update(todo_id):
    """
    Обновляет заголовок списка задач.

    :param todo_id: Идентификатор списка задач.
    :type todo_id: int
    :return: Редирект на главную страницу со списками задач.
    :rtype: flask.Response
    """
    form_data = request.form
    form = TodoCreateForm(**form_data)
    if form.model_validate(form):
        TodoService.update_todo(todo_id, form.title)
    return redirect(url_for('todo_list.index'))


@todo_list_bp.route('/delete/<int:todo_id>', methods=['POST'])
def todo_delete(todo_id):
    """
    Удаляет список задач.

    :param todo_id: Идентификатор списка задач.
    :type todo_id: int
    :return: Редирект на главную страницу со списками задач.
    :rtype: flask.Response
    """
    TodoService.delete_todo(todo_id)
    return redirect(url_for('todo_list.index'))


@todo_list_bp.get('/<int:todo_id>')
def get_todo(todo_id):
    """
    Отображает список задач по его идентификатору.

    :param todo_id: Идентификатор списка задач.
    :type todo_id: int
    :return: HTML-страница со списком задач.
    :rtype: flask.Response
    """
    todo_list = TodoService.get_todo(todo_id)
    if current_user.id != todo_list.user_id:
        abort(403)
    all_tasks, active_tasks, completed_tasks = TodoService.count_tasks(todo_id)
    context = {
        'title': 'Мои задачи',
        'todo_list': todo_list,
        'active_tasks': active_tasks,
        'completed_tasks': completed_tasks,
        'all_tasks': all_tasks
    }
    return render_template('todo_list/todo_list.html', **context)


@todo_list_bp.route('/<int:todo_id>/task-add', methods=['POST'])
def task_add(todo_id):
    """
    Добавляет новую задачу в список задач.

    :param todo_id: Идентификатор списка задач.
    :type todo_id: int
    :return: Редирект на страницу списка задач.
    :rtype: flask.Response
    """
    form_data = request.form
    form = TaskCreateForm(**form_data, todo_id=todo_id)
    if form.model_validate(form):
        TaskService.add_task(form.title, form.description, form.deadline_date, todo_id)
        return redirect(url_for('todo_list.get_todo', todo_id=todo_id))
    return render_template('todo_list/todo_list.html', form=form)


@todo_list_bp.route('/<int:todo_id>/task-update', methods=['POST'])
def task_update(todo_id):
    """
    Обновляет информацию о задаче.

    :param todo_id: Идентификатор списка задач.
    :type todo_id: int
    :return: Редирект на страницу списка задач.
    :rtype: flask.Response
    """
    form_data = request.form
    form = TaskUpdateForm(**form_data)
    if form.model_validate(form):
        TaskService.update_task(form.id, form.title, form.description)
    return redirect(url_for('todo_list.get_todo', todo_id=todo_id))


@todo_list_bp.route('/<int:todo_id>/task-completed', methods=['POST'])
def task_completed(todo_id):
    """
    Помечает задачу как завершенную.

    :param todo_id: Идентификатор списка задач.
    :type todo_id: int
    :return: Редирект на страницу списка задач.
    :rtype: flask.Response
    """
    task_id = request.form.get('task_id')
    TaskService.complete_task(task_id)
    return redirect(url_for('todo_list.get_todo', todo_id=todo_id))


@todo_list_bp.route('/<int:todo_id>/task-delete', methods=['POST'])
def task_delete(todo_id):
    """
    Удаляет задачу из списка задач.

    :param todo_id: Идентификатор списка задач.
    :type todo_id: int
    :return: Редирект на страницу списка задач.
    :rtype: flask.Response
    """
    task_id = request.form.get('task_id')
    TaskService.delete_task(task_id)
    return redirect(url_for('todo_list.get_todo', todo_id=todo_id))
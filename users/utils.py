"""Утилиты для работы с паролями."""

from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """
    Хешировать пароль.

    :param password: Пароль для хеширования.
    :type password: str
    :return: Хешированный пароль.
    :rtype: str
    """
    return generate_password_hash(password)

def verify_password(hashed_password, password):
    """
    Проверить пароль.
    
    :param hashed_password: Хешированный пароль.
    :type hashed_password: str
    :param password: Пароль для проверки.
    :type password: str
    :return: Результат проверки пароля.
    :rtype: bool
    """
    return check_password_hash(hashed_password, password)
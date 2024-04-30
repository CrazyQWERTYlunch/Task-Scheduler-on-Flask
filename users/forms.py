"""Формы для приложения users."""

from pydantic import BaseModel, Field

class ChangePasswordForm(BaseModel):
    """
    Форма для изменения пароля пользователя.

    :param current_password: Текущий пароль пользователя.
    :type current_password: str
    :param new_password: Новый пароль пользователя.
    :type new_password: str
    :param confirm_password: Подтверждение нового пароля пользователя.
    :type confirm_password: str
    """
    current_password: str = Field(..., title="Current Password", max_length=100)
    new_password: str = Field(..., title="New Password", max_length=100)
    confirm_password: str = Field(..., title="Confirm Password", max_length=100)

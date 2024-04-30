"""Модели форм для аутентификации."""

from pydantic import BaseModel, Field, EmailStr

class LoginForm(BaseModel):
    """
    Модель формы для входа.

    Проверяет запрос на вход в систему.
    """

    username: str = Field(title="Имя пользователя", unique=True, max_length=10)
    password: str = Field(title="Пароль", max_length=10)

class RegistrationForm(LoginForm):
    """
    Модель формы для регистрации.

    Проверяет запрос на регистрацию нового пользователя.
    """

    email: EmailStr = Field(title="Email")
    class Config:
        """
        Конфигурация модели.

        Указывает на то, что модель может быть создана из атрибутов.
        """
        from_attributes = True
from pydantic import BaseModel, Field

from tools.fakers import fake


class TokenSchema(BaseModel):  # Добавили структуру с токенами аутентификации
    """
    Описание структуры аутентификационных токенов.
    """
    token_type: str = Field(alias="tokenType")
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")


class LoginResponseSchema(BaseModel):  # Добавили структуру ответа аутентификации
    """
    Описание структуры ответа аутентификации.
    """
    token: TokenSchema


class LoginRequestSchema(BaseModel):
    """
    Описание структуры запроса на аутентификацию.
    """
    email: str = Field(default_factory=fake.email)  # Добавили генерацию случайного email
    password: str = Field(default_factory=fake.password)  # Добавили генерацию случайного пароля


class RefreshRequestSchema(BaseModel):
    """
    Описание структуры запроса для обновления токена.
    """
    refresh_token: str = Field(alias="refreshToken", default_factory=fake.sentence)  # Название ключа совпадает с API
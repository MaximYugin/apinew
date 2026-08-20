from http import HTTPStatus

import pytest
import allure

from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import get_public_users_client, PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from fixtures.users import UserFixture
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
# Импортируем функцию для валидации JSON Schema
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from tools.fakers import fake


@pytest.mark.users  # Добавили маркировку users
@pytest.mark.regression
@allure.tag(AllureTag.USERS, AllureTag.REGRESSION)
class TestUsers:
    @pytest.mark.parametrize('email', ['mail.ru', 'gmail.com', 'example.com'])
    @allure.title("Create user")
    @allure.tag(AllureTag.CREATE_ENTITY)
    def test_create_user(self, public_users_client: PublicUsersClient, email: str):

        # Формируем тело запроса на создание пользователя
        request = CreateUserRequestSchema(email=fake.email(domain=email))
        response = public_users_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)

        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)

        # Проверяем, что данные ответа совпадают с данными запроса
        assert_create_user_response(request, response_data)

        # Проверяем, что тело ответа соответствует ожидаемой JSON-схеме
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.title("Get user me")
    @allure.tag(AllureTag.GET_ENTITY)
    def test_get_user_me(self, function_user: UserFixture, private_users_client: PrivateUsersClient):
        response = private_users_client.get_user_me_api()
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_data, function_user.response)

        validate_json_schema(response.json(), response_data.model_json_schema())
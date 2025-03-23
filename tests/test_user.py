import allure
import pytest
import requests

from helpers import register_new_user_and_return_login_password, generate_random_string
from configuration import AUTH_USER_PATH, AUTH_LOGIN_PATH, AUTH_REGISTER_PATH

@allure.feature('Пользователь')
class TestUser:
    def setup_method(self):
        self.user_access_token = None

    @allure.title('Успешное создание пользователя')
    def test_create_unique_user_success(self):
        user_data = register_new_user_and_return_login_password()
        assert len(user_data) > 0, "Не удалось создать уникального пользователя"
        
        login_response = requests.post(AUTH_LOGIN_PATH, 
            json={"email": user_data[0], "password": user_data[1]})
        assert login_response.status_code == 200
        assert "accessToken" in login_response.json()
        assert "user" in login_response.json()

    @allure.title('Невозможно создать двух одинаковых пользователей')
    def test_cannot_create_duplicate_user(self):
        email = f"{generate_random_string(5)}@{generate_random_string(5)}.ru"
        password = generate_random_string(10)
        name = generate_random_string(10)
        
        payload = {
            "email": email,
            "password": password,
            "name": name
        }

        response = requests.post(AUTH_REGISTER_PATH, json=payload)
        assert response.status_code == 200

        response = requests.post(AUTH_REGISTER_PATH, json=payload)
        assert response.status_code == 403
        assert "user already exists" in response.json()["message"].lower()

    @allure.title('Невозможно создать пользователя без обязательных полей')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_cannot_create_user_without_required_field(self, missing_field):
        payload = {
            "email": f"{generate_random_string(5)}@{generate_random_string(5)}.ru",
            "password": generate_random_string(10),
            "name": generate_random_string(10)
        }

        del payload[missing_field]
        response = requests.post(AUTH_REGISTER_PATH, json=payload)
        assert response.status_code == 403
        assert "required fields" in response.json()["message"].lower()

    @allure.title('Успешная авторизация пользователя')
    def test_user_login_success(self):
        user_data = register_new_user_and_return_login_password()
        assert len(user_data) > 0

        payload = {
            "email": user_data[0],
            "password": user_data[1]
        }

        response = requests.post(AUTH_LOGIN_PATH, json=payload)
        assert response.status_code == 200
        assert "accessToken" in response.json()
        assert "user" in response.json()
        assert "email" in response.json()["user"]
        assert "name" in response.json()["user"]

    @allure.title('Невозможно авторизоваться с неверными учетными данными')
    def test_cannot_login_with_wrong_credentials(self):
        payload = {
            "email": f"{generate_random_string(5)}@{generate_random_string(5)}.ru",
            "password": generate_random_string(10)
        }

        response = requests.post(AUTH_LOGIN_PATH, json=payload)
        assert response.status_code == 401
        assert "email or password are incorrect" == response.json()["message"].lower()

    @allure.title('Невозможно авторизоваться без обязательных полей')
    @pytest.mark.parametrize('missing_field', ['email', 'password'])
    def test_cannot_login_without_required_field(self, missing_field):
        payload = {
            "email": f"{generate_random_string(5)}@{generate_random_string(5)}.ru",
            "password": generate_random_string(10)
        }

        del payload[missing_field]
        response = requests.post(AUTH_LOGIN_PATH, json=payload)
        assert response.status_code == 401
        assert "email or password are incorrect" == response.json()["message"].lower()

    @allure.title('Успешное обновление данных авторизованного пользователя')
    @pytest.mark.parametrize('field', ['email', 'name'])
    def test_update_authorized_user_data_success(self, field):
        email, password, name = register_new_user_and_return_login_password()
        assert email is not None

        auth_payload = {
            "email": email,
            "password": password
        }
        auth_response = requests.post(AUTH_LOGIN_PATH, json=auth_payload)
        assert auth_response.status_code == 200
        token = auth_response.json().get("accessToken")

        new_value = generate_random_string(10)
        if field == "email":
            new_value = f"{new_value}@example.com"
        
        update_payload = {field: new_value}
        headers = {"Authorization": token}
        
        response = requests.patch(AUTH_USER_PATH, json=update_payload, headers=headers)
        assert response.status_code == 200
        assert response.json()["user"][field] == new_value

    @allure.title('Невозможно обновить данные без авторизации')
    @pytest.mark.parametrize('field', ['email', 'name'])
    def test_update_unauthorized_user_data_fails(self, field):
        new_value = generate_random_string(10)
        if field == "email":
            new_value = f"{new_value}@example.com"
        
        update_payload = {field: new_value}
        response = requests.patch(AUTH_USER_PATH, json=update_payload)
        
        assert response.status_code == 401
        assert "you should be authorised" in response.json()["message"].lower()
import allure
import pytest
import requests

from helpers import register_new_user_and_return_login_password, generate_random_string
from configuration import AUTH_USER_PATH, AUTH_LOGIN_PATH, AUTH_REGISTER_PATH

@allure.feature('Пользователь')
class TestUser:
    def setup_method(self):
        self.user_id = None
        self.user_access_token = None

    def teardown_method(self):
        if self.user_id:
            requests.delete(f"{AUTH_USER_PATH}/{self.user_id}")

    @allure.title('Успешное создание пользователя')
    def test_create_unique_user_success(self):
        user_data = register_new_user_and_return_login_password()
        assert len(user_data) > 0, "Не удалось создать уникального пользователя"
        
        login_response = requests.post(AUTH_LOGIN_PATH, 
            json={"login": user_data[0], "password": user_data[1]})
        self.user_id = login_response.json()["id"]

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
        assert response.status_code == 201

        login_response = requests.post(AUTH_LOGIN_PATH, 
            json={"email": email, "password": password})
        self.user_id = login_response.json()["id"]

        response = requests.post(AUTH_REGISTER_PATH, json=payload)
        assert response.status_code == 403
        assert "already exists" in response.json()["message"].lower()

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
        assert "id" in response.json()

        self.user_id = response.json()["id"]

    @allure.title('Невозможно авторизоваться с неверными учетными данными')
    def test_cannot_login_with_wrong_credentials(self):
        payload = {
            "email": f"{generate_random_string(5)}@{generate_random_string(5)}.ru",
            "password": generate_random_string(10)
        }

        response = requests.post(AUTH_LOGIN_PATH, json=payload)
        assert response.status_code == 401
        assert "not found" in response.json()["message"].lower()

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
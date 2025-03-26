import allure
import requests

from helpers import register_new_user_and_return_login_password, delete_user
from configuration import ORDERS_PATH, INGREDIENTS_PATH, AUTH_LOGIN_PATH, ERROR_MESSAGES

@allure.feature('Заказ')
class TestOrder:
    def setup_method(self):
        self.token = None
        self.email = None
        self.password = None

    def teardown_method(self):
        delete_user(self.token)

    def get_ingredients(self):
        response = requests.get(INGREDIENTS_PATH)
        assert response.status_code == 200
        return [item["_id"] for item in response.json()["data"][:2]]  # Берем первые 2 ингредиента

    @allure.title('Создание заказа с авторизацией')
    def test_create_order_with_auth(self):
        user_data = register_new_user_and_return_login_password()
        self.email, self.password = user_data[0], user_data[1]
        auth_response = requests.post(AUTH_LOGIN_PATH, json={"email": self.email, "password": self.password})
        assert auth_response.status_code == 200
        self.token = auth_response.json().get("accessToken")

        ingredients = self.get_ingredients()
        headers = {"Authorization": self.token}
        response = requests.post(ORDERS_PATH, json={"ingredients": ingredients}, headers=headers)
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title('Создание заказа без авторизации')
    def test_create_order_without_auth(self):
        ingredients = self.get_ingredients()
        response = requests.post(ORDERS_PATH, json={"ingredients": ingredients})
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self):
        response = requests.post(ORDERS_PATH, json={"ingredients": []})
        
        assert response.status_code == 400
        assert response.json()["success"] is False
        assert ERROR_MESSAGES["INVALID_INGREDIENTS"] == response.json()["message"].lower()

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_with_invalid_ingredients(self):
        invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]
        response = requests.post(ORDERS_PATH, json={"ingredients": invalid_ingredients})
        
        assert response.status_code == 500

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_orders_with_auth(self):
        user_data = register_new_user_and_return_login_password()
        self.email, self.password = user_data[0], user_data[1]
        auth_response = requests.post(AUTH_LOGIN_PATH, json={"email": self.email, "password": self.password})
        assert auth_response.status_code == 200
        self.token = auth_response.json().get("accessToken")

        ingredients = self.get_ingredients()
        headers = {"Authorization": self.token}
        create_response = requests.post(ORDERS_PATH, json={"ingredients": ingredients}, headers=headers)
        assert create_response.status_code == 200

        response = requests.get(ORDERS_PATH, headers=headers)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "orders" in response.json()

    @allure.title('Получение заказов без авторизации')
    def test_get_orders_without_auth(self):
        response = requests.get(ORDERS_PATH)
        
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert ERROR_MESSAGES["UNAUTHORIZED"] == response.json()["message"].lower()
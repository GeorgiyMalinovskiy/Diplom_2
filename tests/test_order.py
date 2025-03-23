import allure
import pytest
import requests

from helpers import register_new_user_and_return_login_password
from configuration import ORDERS_PATH, INGREDIENTS_PATH, AUTH_LOGIN_PATH

@allure.feature('Заказ')
class TestOrder:
    def setup_method(self):
        self.token = None

    def get_ingredients(self):
        response = requests.get(INGREDIENTS_PATH)
        assert response.status_code == 200
        return [item["_id"] for item in response.json()["data"][:2]]  # Берем первые 2 ингредиента

    @allure.title('Создание заказа с авторизацией')
    def test_create_order_with_auth(self):
        email, password, _ = register_new_user_and_return_login_password()
        auth_response = requests.post(AUTH_LOGIN_PATH, json={"email": email, "password": password})
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
        assert "ingredient ids must be provided" == response.json()["message"].lower()

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_with_invalid_ingredients(self):
        invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]
        response = requests.post(ORDERS_PATH, json={"ingredients": invalid_ingredients})
        
        assert response.status_code == 500

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_orders_with_auth(self):
        email, password, _ = register_new_user_and_return_login_password()
        auth_response = requests.post(AUTH_LOGIN_PATH, json={"email": email, "password": password})
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
        assert "you should be authorised" == response.json()["message"].lower()
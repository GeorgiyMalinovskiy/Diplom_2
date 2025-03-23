import allure
import pytest
import requests

@allure.feature('Заказ')
class TestOrder:
    def setup_method(self):
        self.id = None
import pytest
from helpers import generate_random_string

@pytest.fixture
def register_payload():
    email = f"{generate_random_string(5)}@{generate_random_string(5)}.ru"
    name = generate_random_string(10)
    password = generate_random_string(10)

    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    return payload


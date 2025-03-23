import random
import string
import requests

from configuration import AUTH_REGISTER_PATH

def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def register_new_user_and_return_login_password():
    email = f"{generate_random_string(5)}@{generate_random_string(5)}.ru"
    name = generate_random_string(10)
    password = generate_random_string(10)

    payload = {
        "email": email,
        "name": name,
        "password": password
    }

    response = requests.post(AUTH_REGISTER_PATH, json=payload, timeout=5)

    if response.status_code == 201:
        response.json()

    return {}
    
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
        "password": password,
        "name": name
    }

    try:
        response = requests.post(AUTH_REGISTER_PATH, json=payload, timeout=5)
        if response.status_code == 200:
            return email, password, name
    except Exception as e:
        print(f"Error during registration: {e}")
    
    return None, None, None
    
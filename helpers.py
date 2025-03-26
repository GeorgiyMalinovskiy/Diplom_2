import random
import string
import requests

from configuration import AUTH_REGISTER_PATH, AUTH_LOGIN_PATH, AUTH_USER_PATH

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

def login_user(email, password):
    try:
        response = requests.post(AUTH_LOGIN_PATH, json={"email": email, "password": password})
        if response.status_code == 200:
            return response.json().get("accessToken")
    except Exception as e:
        print(f"Error during login: {e}")
    return None

def delete_user(token):
    if not token:
        return
    try:
        headers = {"Authorization": token}
        requests.delete(AUTH_USER_PATH, headers=headers)
    except Exception as e:
        print(f"Error during user deletion: {e}")
    
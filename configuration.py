BASE_URL = "https://stellarburgers.nomoreparties.site/api"
INGREDIENTS_PATH = f"{BASE_URL}/ingredients"
ORDERS_PATH = f"{BASE_URL}/orders"
ORDERS_ALL_PATH = f"{ORDERS_PATH}/all"
PASSWORD_RESET_PATH = f"{BASE_URL}/password-reset"
AUTH_REGISTER_PATH = f"{BASE_URL}/auth/register"
AUTH_LOGIN_PATH = f"{BASE_URL}/auth/login"
AUTH_LOGOUT_PATH = f"{BASE_URL}/auth/logout"
AUTH_TOKEN_PATH = f"{BASE_URL}/auth/token"
AUTH_USER_PATH = f"{BASE_URL}/auth/user"

ERROR_MESSAGES = {
    "USER_ALREADY_EXISTS": "user already exists",
    "REQUIRED_FIELDS": "required fields",
    "WRONG_CREDENTIALS": "wrong credentials",
    "UNAUTHORIZED": "you should be authorised",
    "INVALID_LOGIN_OR_PASSWORD": "email or password are incorrect",
    "INVALID_INGREDIENTS": "ingredient ids must be provided"
}
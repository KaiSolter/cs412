import json
import os

import requests


LOGIN_API_URL = "https://cs-webapps.bu.edu/ksolter/mini_insta/api/login/"


def print_response(label, response):
    print(f"\n[{label}] {response.request.method} {response.url}")
    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))
    try:
        print("Body:", json.dumps(response.json(), indent=2))
    except ValueError:
        print("Body:", response.text[:800])


def test_login_invalid_credentials():
    payload = {
        "username": "not_a_real_user",
        "password": "wrong_password",
    }
    response = requests.post(LOGIN_API_URL, json=payload, timeout=20)
    print_response("LOGIN_INVALID", response)


def test_login_with_env_credentials():
    username = os.getenv("MINI_INSTA_USERNAME")
    password = os.getenv("MINI_INSTA_PASSWORD")

    if not username or not password:
        print(
            "\n[LOGIN_VALID] Skipped: set MINI_INSTA_USERNAME and MINI_INSTA_PASSWORD to test valid login."
        )
        return

    payload = {
        "username": username,
        "password": password,
    }
    response = requests.post(LOGIN_API_URL, json=payload, timeout=20)
    print_response("LOGIN_VALID", response)

    if response.ok:
        data = response.json()
        token = data.get("token")
        if token:
            print("Token received: yes")
        else:
            print("Token received: no")


if __name__ == "__main__":
    try:
        test_login_invalid_credentials()
        test_login_with_env_credentials()
    except requests.exceptions.RequestException as err:
        print("\nNetwork/request error:", err)
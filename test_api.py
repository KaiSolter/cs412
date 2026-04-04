import json
import requests


API_URL = "https://cs-webapps.bu.edu/ksolter/dadjokes/api/jokes/"


def print_response(label, response):
    print(f"\n[{label}] {response.request.method} {response.url}")
    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))
    try:
        print("Body:", json.dumps(response.json(), indent=2))
    except ValueError:
        print("Body:", response.text[:800])


def test_get():
    response = requests.get(API_URL, timeout=20)
    print_response("GET", response)


def test_post_joke():
    data = {
        "text": "Why don't skeletons fight each other? They don't have the guts!",
        "contributer": "Anon",
    }
    response = requests.post(API_URL, json=data, timeout=20)
    print_response("POST", response)


if __name__ == "__main__":
    try:
        test_get()
        test_post_joke()
    except requests.exceptions.RequestException as err:
        print("\nNetwork/request error:", err)
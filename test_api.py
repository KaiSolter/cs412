import requests 

def test_post_joke():
    url = "http://cs-webapps.bu.edu/ksolter/dadjokes/api/jokes/"
    data = {
        "text": "Why don't skeletons fight each other? They don't have the guts!",
        "contributer": "Anon"
    }

    try:
        response = requests.post(url, json=data)
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    test_post_joke()
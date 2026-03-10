import json
import time
import requests

SERVER_URL = "http://127.0.0.1:8000/checkin"
PROFILE_FILE = "profile.json"

def load_profile():
    with open(PROFILE_FILE, "r") as f:
        return json.load(f)

def send_checkin(profile):
    try:
        response = requests.post(SERVER_URL, json=profile)
        print("Status:", response.status_code)
        print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error:", e)

def main():
    profile = load_profile()

    while True:
        send_checkin(profile)
        time.sleep(10)

if __name__ == "__main__":
    main()
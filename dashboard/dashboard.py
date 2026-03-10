import requests
import time

SERVER_URL = "http://127.0.0.1:8000/agents"

def show_agents():

    try:
        response = requests.get(SERVER_URL)
        data = response.json()

        print("\n====== ACTIVE AGENTS ======")
        print(f"Total agents: {data['count']}\n")

        for agent in data["agents"]:
            print("Hostname:", agent["hostname"])
            print("User:", agent["username"])
            print("IP:", agent["ip"])
            print("OS:", agent["os"])
            print("Last Check-in:", agent["last_checkin"])
            print("-----------------------------")

    except Exception as e:
        print("Error:", e)


def main():

    while True:
        show_agents()
        time.sleep(5)


if __name__ == "__main__":
    main()
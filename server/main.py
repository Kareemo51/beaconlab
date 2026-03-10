from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "beacons.log")

class AgentCheckin(BaseModel):
    hostname: str
    username: str
    os: str
    ip: str

def log_beacon(message):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

def parse_agents():
    agents = {}

    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or not line.startswith("["):
                continue

            try:
                timestamp = line.split("]")[0].strip("[")
                rest = line.split("] ", 1)[1]
                hostname, username, ip, os_name = [part.strip() for part in rest.split(" | ", 3)]

                agents[hostname] = {
                    "hostname": hostname,
                    "username": username,
                    "ip": ip,
                    "os": os_name,
                    "last_checkin": timestamp
                }
            except (IndexError, ValueError):
                continue

    return list(agents.values())

@app.get("/")
def home():
    return {"message": "BeaconLab server is running"}

@app.post("/checkin")
def checkin(agent: AgentCheckin):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{now}] {agent.hostname} | {agent.username} | {agent.ip} | {agent.os}"

    print(message)
    log_beacon(message)

    return {
        "status": "received",
        "message": f"Hello {agent.hostname}"
    }

@app.get("/agents")
def get_agents():
    return {
        "count": len(parse_agents()),
        "agents": parse_agents()
    }
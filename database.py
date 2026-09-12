import os
import json
import base64
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")
GITHUB_FILE = "data.json"

API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}"

def _headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

def _default_data():
    return {
        "countries": {},
        "statements": [],
        "chat": [],
        "last_tick": 0
    }

def load_data():
    """خواندن data.json از گیت‌هاب"""
    if not GITHUB_TOKEN or not GITHUB_REPO:
        print("GITHUB_TOKEN یا GITHUB_REPO تنظیم نشده!")
        return _default_data()
    try:
        r = requests.get(API_URL, headers=_headers(), timeout=10)
        if r.status_code == 200:
            content = r.json()["content"]
            decoded = base64.b64decode(content).decode("utf-8")
            return json.loads(decoded)
        else:
            print(f"load_data status: {r.status_code}")
            return _default_data()
    except Exception as e:
        print(f"Error loading data: {e}")
        return _default_data()

def save_data(data):
    """ذخیره data.json در گیت‌هاب"""
    if not GITHUB_TOKEN or not GITHUB_REPO:
        return False
    try:
        r = requests.get(API_URL, headers=_headers(), timeout=10)
        sha = r.json().get("sha") if r.status_code == 200 else None
        
        encoded = base64.b64encode(
            json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        ).decode("utf-8")
        
        payload = {"message": "Update game data", "content": encoded}
        if sha:
            payload["sha"] = sha
        
        r = requests.put(API_URL, headers=_headers(), json=payload, timeout=10)
        return r.status_code in [200, 201]
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

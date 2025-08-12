import requests
from typing import Dict, Any

API_URL = "http://127.0.0.1:5000"

def login(email: str, password: str) -> Dict[str, Any]:
    url = f"{API_URL}/login"
    data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def check_session(token: str) -> Dict[str, Any]:
    url = f"{API_URL}/session"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
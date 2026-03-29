import os
import requests
from jose import jwt
from datetime import datetime, timedelta

# Auth configuration from auth.py
SECRET_KEY = "mysecretkey_change_in_production"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Create a token for a user that exists in the DB
# Let's hope 'test@example.com' or similar exists, or I'll just check models
token = create_access_token({"sub": "parv@gmail.com"})

# Test the chat endpoint
try:
    response = requests.post(
        "http://localhost:8000/api/chat",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "messages": [{"role": "user", "content": "hi"}],
            "language": "en"
        },
        timeout=10
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

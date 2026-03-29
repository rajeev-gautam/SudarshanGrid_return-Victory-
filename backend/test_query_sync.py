import requests
import time
import sqlite3
import os
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

token = create_access_token({"sub": "parv@gmail.com"})

# Submit a query
try:
    print("Submitting query...")
    response = requests.post(
        "http://localhost:8000/api/queries",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "subject": "Verification Test",
            "message": "Testing the auto-acknowledgement status update."
        },
        timeout=10
    )
    print(f"Post Status: {response.status_code}")
    query_id = response.json().get('id')
    print(f"Query ID: {query_id}")

    # The email sending is a background task. Give it some time.
    print("Waiting for background task (email)...")
    time.sleep(5) 

    # Check status in DB
    conn = sqlite3.connect('backend/govr.db')
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM support_queries WHERE id = ?', (query_id,))
    res = cursor.fetchone()
    print(f"Query Status in DB: {res[0] if res else 'Not Found'}")
    conn.close()

except Exception as e:
    print(f"Error: {e}")

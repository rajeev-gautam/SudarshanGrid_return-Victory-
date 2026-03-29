import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("VITE_GROQ_API_KEY")
MODEL = os.getenv("VITE_GROQ_MODEL", "llama-3.3-70b-versatile")

print(f"Using Model: {MODEL}")
print(f"API Key present: {bool(GROQ_API_KEY)}")

try:
    response = requests.post(
        GROQ_API_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "user", "content": "hi"}
            ]
        },
        timeout=10
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

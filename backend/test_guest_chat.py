import requests

# Test the chat endpoint WITHOUT a token
try:
    response = requests.post(
        "http://localhost:8000/api/chat",
        headers={
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

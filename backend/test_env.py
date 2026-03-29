import os
from dotenv import load_dotenv

# Try relative to CWD
print(f"CWD: {os.getcwd()}")
load_dotenv()
print(f"VITE_GROQ_API_KEY (cwd): {os.getenv('VITE_GROQ_API_KEY')}")

# Try absolute path
env_path = os.path.join(os.path.dirname(__file__), "../.env")
print(f"Loading from: {env_path}")
load_dotenv(env_path)
print(f"VITE_GROQ_API_KEY (absolute): {os.getenv('VITE_GROQ_API_KEY')}")

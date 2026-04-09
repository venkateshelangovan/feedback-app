import os
from dotenv import load_dotenv, find_dotenv

# Try to find the .env file
env_path = os.path.join(os.path.dirname(__file__), "backend", ".env")
print(f"Checking path: {env_path}")
print(f"Exists: {os.path.exists(env_path)}")

if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    print(f"Token loaded: {'Yes' if token else 'No'}")
    if token:
        print(f"Token starts with: {token[:10]}...")
    print(f"Chat ID loaded: {'Yes' if chat_id else 'No'}")
    if chat_id:
        print(f"Chat ID: {chat_id}")
else:
    print("Could not find .env file at specified path.")

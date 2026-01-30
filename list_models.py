import os
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "AIzaSyAYR6STJoLyDqO8ngNhsP7-pahnDCsmzr8"))

try:
    print("Listing models...")
    with open("models.txt", "w") as f:
        for m in client.models.list():
            f.write(f"{m.name}\n")
    print("Models listed to models.txt")
except Exception as e:
    print(f"Error listing models: {e}")

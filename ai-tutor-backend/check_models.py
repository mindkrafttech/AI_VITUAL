from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GOOGLE_API_KEY")
if not key:
    print("ERROR: GOOGLE_API_KEY not found in .env file.")
    exit(1)

print(f"Testing Key: {key[:10]}...")

print("\n--- CHECKING NEW SDK (google-genai) ---")
try:
    from google import genai
    client = genai.Client(api_key=key)
    print("Available Models:")
    for model in client.models.list():
        print(f"  > {model.name}")
except Exception as e:
    print(f"New SDK Error: {e}")

print("\n--- CHECKING LEGACY SDK (google-generativeai) ---")
try:
    import google.generativeai as genai_legacy
    genai_legacy.configure(api_key=key)
    print("Available Models:")
    for model in genai_legacy.list_models():
        print(f"  > {model.name}")
except Exception as e:
    print(f"Legacy SDK Error: {e}")

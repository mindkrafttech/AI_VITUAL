import requests
import json

def test_research():
    url = "http://127.0.0.1:5000/api/ai/research"
    payload = {"topic": "Artificial Intelligence"}
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        print("Response Content:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_research()

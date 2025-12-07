import requests
import json

url = "http://localhost:8000/chat"

payload = {
    "character_file": "data/characters/astra.yaml",
    "enable_user_memory": True,
    "user_name": "Jordan",
    "user_interests": "space exploration and adventure",
    "message": "Where are you now?",
    "model": "gpt-4-turbo",
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response:")
print(json.dumps(response.json(), indent=2))

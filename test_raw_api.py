import requests
import json

# Test the raw API response
response = requests.get("http://localhost:8002/processes")
print(f"Status: {response.status_code}")
print(f"Raw response: {response.text}")

if response.status_code == 200:
    try:
        data = response.json()
        print("\nParsed JSON:")
        print(json.dumps(data, indent=2))
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")

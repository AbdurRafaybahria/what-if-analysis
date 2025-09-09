import requests
import json

# Test API processes endpoint
response = requests.get("http://localhost:8002/processes")
print(f"Status: {response.status_code}")
data = response.json()
print(f"Processes found: {len(data['processes'])}")

for process in data['processes']:
    print(f"- ID: {process['id']}")
    print(f"  Name: {process['name']}")
    print(f"  Tasks: {process['tasks_count']}")
    print()

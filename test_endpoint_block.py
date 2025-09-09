import requests
import json

# Test that cms-process is properly blocked
print("Testing /optimize/cms-process endpoint...")
print("=" * 50)

# Test with empty body
response1 = requests.post("http://localhost:8002/optimize/cms-process", json={})
print(f"Empty body - Status: {response1.status_code}")
if response1.status_code != 200:
    print(f"Response: {response1.text}")

print()

# Test with some data
test_data = {"process_id": 1, "process_name": "test"}
response2 = requests.post("http://localhost:8002/optimize/cms-process", json=test_data)
print(f"With data - Status: {response2.status_code}")
if response2.status_code != 200:
    print(f"Response: {response2.text}")

print()
print("Expected: 404 with message about endpoint not found")

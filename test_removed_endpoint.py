import requests
import json

# Test that the legacy endpoint is removed
legacy_url = "http://localhost:8002/optimize/cms-process"
test_data = {
    "process_id": 7,
    "process_name": "Test Process",
    "process_tasks": []
}

print("Testing removed legacy endpoint...")
print(f"URL: {legacy_url}")
print("=" * 50)

try:
    response = requests.post(legacy_url, json=test_data, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 404:
        print("SUCCESS: Legacy endpoint properly removed (404)")
    elif response.status_code == 405:
        print("SUCCESS: Legacy endpoint properly removed (405 Method Not Allowed)")
    else:
        print(f"UNEXPECTED: Endpoint still exists - Status: {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

# Test that the new endpoint with ID still works
new_url = "http://localhost:8002/optimize/cms-process/7"
print(f"\nTesting new endpoint with ID...")
print(f"URL: {new_url}")
print("=" * 50)

try:
    response = requests.post(new_url, timeout=30)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("SUCCESS: New endpoint with ID still working")
    else:
        print(f"ERROR: New endpoint failed - Status: {response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

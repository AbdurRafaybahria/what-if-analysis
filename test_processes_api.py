import requests
import json

# Test the updated /processes endpoint - fresh request
response = requests.get("http://localhost:8002/processes")
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    processes = data['processes']
    
    print(f"\nTotal processes found: {len(processes)}")
    print("=" * 60)
    
    for i, process in enumerate(processes, 1):
        print(f"{i}. {process['name']}")
        print(f"   ID: {process['id']}")
        print(f"   Company: {process['company']}")
        print(f"   Type: {process['type']}")
        print(f"   Tasks: {process['tasks_count']}")
        if process['type'] == 'cms':
            print(f"   Description: {process['description'][:100]}...")
            # Show actual process_id from CMS data
            if 'process_data' in process:
                print(f"   CMS Process ID: {process['process_data']['process_id']}")
        print()
else:
    print(f"Error: {response.status_code}")
    print(response.text)

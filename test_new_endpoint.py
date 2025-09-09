import requests
import json

# Test new CMS integration endpoint with process ID
process_id = 7
url = f"http://localhost:8002/optimize/cms-process/{process_id}"

print(f"Testing new CMS optimization endpoint for process ID: {process_id}")
print(f"URL: {url}")
print("=" * 60)

try:
    # Test the new endpoint that fetches process data by ID
    response = requests.post(url, timeout=60)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("SUCCESS: Optimization successful!")
        print(f"Process: {result.get('process_name', 'Unknown')}")
        print(f"Scenarios generated: {len(result.get('scenarios', []))}")
        
        if 'scenarios' in result:
            for i, scenario in enumerate(result['scenarios'], 1):
                print(f"\nScenario {i}: {scenario.get('name', 'Unnamed')}")
                print(f"  Duration: {scenario.get('total_duration_hours', 0):.1f} hours")
                print(f"  Cost: ${scenario.get('total_cost', 0):.2f}")
                if 'tasks' in scenario:
                    print(f"  Tasks: {len(scenario['tasks'])}")
                    
        # Show transformation summary if available
        if 'transformation_summary' in result:
            summary = result['transformation_summary']
            print(f"\nTransformation Summary:")
            print(f"  Tasks converted: {summary.get('tasks_converted', 0)}")
            print(f"  Resources converted: {summary.get('resources_converted', 0)}")
            print(f"  Total duration: {summary.get('total_duration_hours', 0):.1f} hours")
            
    elif response.status_code == 404:
        print(f"ERROR: Process not found")
        print(f"Response: {response.text}")
    else:
        print(f"ERROR: Status {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"ERROR: Request failed - {e}")
except Exception as e:
    print(f"ERROR: Unexpected error - {e}")

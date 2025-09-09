import requests
import json

# Get the OpenAPI spec to see all endpoints
response = requests.get("http://localhost:8002/openapi.json")
if response.status_code == 200:
    openapi = response.json()
    paths = openapi.get("paths", {})
    
    print("All API endpoints:")
    print("=" * 50)
    
    for path, methods in paths.items():
        for method, details in methods.items():
            summary = details.get("summary", "No summary")
            print(f"{method.upper()} {path} - {summary}")
    
    # Check specifically for cms-process endpoints
    print("\nCMS Process endpoints:")
    print("=" * 30)
    
    cms_endpoints = [path for path in paths.keys() if "cms-process" in path]
    if cms_endpoints:
        for endpoint in cms_endpoints:
            print(f"Found: {endpoint}")
    else:
        print("No cms-process endpoints found")
        
else:
    print(f"Failed to get OpenAPI spec: {response.status_code}")

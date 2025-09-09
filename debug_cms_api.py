import httpx
import asyncio
import json

async def test_cms_api():
    """Test CMS API directly to debug the issue"""
    try:
        print("Testing CMS API authentication...")
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test authentication
            auth_response = await client.post(
                "https://server-digitaltwin-enterprise-production.up.railway.app/auth/login",
                json={
                    "email": "superadmin@example.com",
                    "password": "ChangeMe123!"
                }
            )
            
            print(f"Auth Status: {auth_response.status_code}")
            
            if auth_response.status_code == 200:
                auth_data = auth_response.json()
                access_token = auth_data['access_token']
                print("Authentication successful!")
                
                # Test processes endpoint
                print("\nFetching processes...")
                processes_response = await client.get(
                    "https://server-digitaltwin-enterprise-production.up.railway.app/process/with-relations",
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                
                print(f"Processes Status: {processes_response.status_code}")
                
                if processes_response.status_code == 200:
                    processes = processes_response.json()
                    print(f"Found {len(processes)} CMS processes:")
                    
                    for process in processes:
                        print(f"- {process['process_name']} (ID: {process['process_id']}) - {process['company']['name']}")
                        print(f"  Tasks: {len(process.get('process_tasks', []))}")
                    
                    return processes
                else:
                    print(f"Failed to fetch processes: {processes_response.text}")
            else:
                print(f"Authentication failed: {auth_response.text}")
                
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    result = asyncio.run(test_cms_api())

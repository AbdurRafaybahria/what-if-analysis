"""
Test script for CMS integration with What-If Analysis
"""
import requests
import json

# CMS sample data from the user
cms_data = {
    "process_id": 7,
    "process_name": "E-Commerce Platform Development",
    "process_code": "ECPD-001",
    "company_id": 2,
    "capacity_requirement_minutes": 207,
    "process_overview": "Build a modern e-commerce platform with user management, product, catalog, and payment processing.",
    "parent_process_id": None,
    "parent_task_id": None,
    "created_at": "2025-09-08T06:56:14.275Z",
    "updated_at": "2025-09-08T06:56:35.970Z",
    "company": {
        "company_id": 2,
        "companyCode": "CSP",
        "name": "Crystal System Pakistan",
        "created_by": 1,
        "created_at": "2025-08-28T15:59:06.000Z",
        "updated_at": "2025-08-29T05:54:25.064Z"
    },
    "parent_process": None,
    "parent_task": None,
    "process_tasks": [
        {
            "process_id": 7,
            "task_id": 10,
            "order": 1,
            "task": {
                "task_id": 10,
                "task_name": "Database Design and Setup",
                "task_code": "DBDS-01",
                "task_company_id": 2,
                "task_capacity_minutes": 32,
                "task_process_id": None,
                "task_overview": "Design database schema and set up initial database structure.",
                "created_at": "2025-09-08T06:38:16.043Z",
                "updated_at": "2025-09-08T06:38:16.043Z",
                "jobTasks": [
                    {
                        "job_id": 11,
                        "task_id": 10,
                        "job": {
                            "job_id": 11,
                            "jobCode": "DBA-01",
                            "name": "Database Admin",
                            "description": "Database design and optimization specialist.",
                            "hourlyRate": 88,
                            "maxHoursPerDay": 6,
                            "function_id": 3,
                            "company_id": 2,
                            "job_level_id": 3,
                            "createdAt": "2025-09-08T06:34:02.081Z",
                            "updatedAt": "2025-09-08T06:34:02.081Z"
                        }
                    }
                ]
            }
        },
        {
            "process_id": 7,
            "task_id": 11,
            "order": 2,
            "task": {
                "task_id": 11,
                "task_name": "User Authentication",
                "task_code": "UA-01",
                "task_company_id": 2,
                "task_capacity_minutes": 24,
                "task_process_id": None,
                "task_overview": "Implement user registration login and authentication.",
                "created_at": "2025-09-08T06:43:04.108Z",
                "updated_at": "2025-09-08T06:43:04.108Z",
                "jobTasks": [
                    {
                        "job_id": 6,
                        "task_id": 11,
                        "job": {
                            "job_id": 6,
                            "jobCode": "SB-01",
                            "name": "Senior Backend",
                            "description": "Lead Backend developer with API experitse.",
                            "hourlyRate": 94,
                            "maxHoursPerDay": 8,
                            "function_id": 3,
                            "company_id": 2,
                            "job_level_id": 4,
                            "createdAt": "2025-09-08T06:15:00.339Z",
                            "updatedAt": "2025-09-08T06:15:00.339Z"
                        }
                    }
                ]
            }
        },
        {
            "process_id": 7,
            "task_id": 12,
            "order": 3,
            "task": {
                "task_id": 12,
                "task_name": "Product Catalog API",
                "task_code": "PCAPI-01",
                "task_company_id": 2,
                "task_capacity_minutes": 40,
                "task_process_id": None,
                "task_overview": "Build Rest APIs for product management and catalog.",
                "created_at": "2025-09-08T06:45:29.194Z",
                "updated_at": "2025-09-08T06:45:29.194Z",
                "jobTasks": [
                    {
                        "job_id": 8,
                        "task_id": 12,
                        "job": {
                            "job_id": 8,
                            "jobCode": "FSD-01",
                            "name": "Fullstack Developer",
                            "description": "Versatile developer with both frontend and backend skills.",
                            "hourlyRate": 80,
                            "maxHoursPerDay": 8,
                            "function_id": 3,
                            "company_id": 2,
                            "job_level_id": 3,
                            "createdAt": "2025-09-08T06:26:59.233Z",
                            "updatedAt": "2025-09-08T06:26:59.233Z"
                        }
                    }
                ]
            }
        },
        {
            "process_id": 7,
            "task_id": 13,
            "order": 4,
            "task": {
                "task_id": 13,
                "task_name": "Frontend UI",
                "task_code": "FUI-01",
                "task_company_id": 2,
                "task_capacity_minutes": 47,
                "task_process_id": None,
                "task_overview": "Create a responsive frontend with React/Vue.",
                "created_at": "2025-09-08T06:47:33.469Z",
                "updated_at": "2025-09-08T06:47:33.469Z",
                "jobTasks": [
                    {
                        "job_id": 7,
                        "task_id": 13,
                        "job": {
                            "job_id": 7,
                            "jobCode": "FD-01",
                            "name": "Frontend Developer",
                            "description": "Frontend specialist with modern frameworks",
                            "hourlyRate": 85,
                            "maxHoursPerDay": 8,
                            "function_id": 3,
                            "company_id": 2,
                            "job_level_id": 3,
                            "createdAt": "2025-09-08T06:21:36.188Z",
                            "updatedAt": "2025-09-08T06:21:36.188Z"
                        }
                    }
                ]
            }
        },
        {
            "process_id": 7,
            "task_id": 14,
            "order": 5,
            "task": {
                "task_id": 14,
                "task_name": "Payment Integration",
                "task_code": "PI-01",
                "task_company_id": 2,
                "task_capacity_minutes": 28,
                "task_process_id": None,
                "task_overview": "Integrate Payment gateways and checkout process.",
                "created_at": "2025-09-08T06:50:49.180Z",
                "updated_at": "2025-09-08T06:50:49.180Z",
                "jobTasks": [
                    {
                        "job_id": 9,
                        "task_id": 14,
                        "job": {
                            "job_id": 9,
                            "jobCode": "PS-01",
                            "name": "Payment Specialist",
                            "description": "Specialist in payment gateway integration",
                            "hourlyRate": 99,
                            "maxHoursPerDay": 6,
                            "function_id": 3,
                            "company_id": 2,
                            "job_level_id": 4,
                            "createdAt": "2025-09-08T06:29:35.322Z",
                            "updatedAt": "2025-09-08T06:29:35.322Z"
                        }
                    }
                ]
            }
        },
        {
            "process_id": 7,
            "task_id": 15,
            "order": 6,
            "task": {
                "task_id": 15,
                "task_name": "Testing and QA",
                "task_code": "TQA-01",
                "task_company_id": 2,
                "task_capacity_minutes": 36,
                "task_process_id": None,
                "task_overview": "Comprehensive testing including unit integration and system level testing.",
                "created_at": "2025-09-08T06:52:39.166Z",
                "updated_at": "2025-09-08T06:52:39.166Z",
                "jobTasks": [
                    {
                        "job_id": 10,
                        "task_id": 15,
                        "job": {
                            "job_id": 10,
                            "jobCode": "QAE-01",
                            "name": "QA Engineer",
                            "description": "Quality assurance and test automation expert.",
                            "hourlyRate": 75,
                            "maxHoursPerDay": 7,
                            "function_id": 3,
                            "company_id": 2,
                            "job_level_id": 3,
                            "createdAt": "2025-09-08T06:31:50.065Z",
                            "updatedAt": "2025-09-08T06:31:50.065Z"
                        }
                    }
                ]
            }
        }
    ]
}

def test_cms_endpoint():
    """Test the CMS optimization endpoint"""
    
    # API endpoint - using process ID from CMS data
    process_id = cms_data.get('process_id', 7)  # Default to 7 if not found
    url = f"http://localhost:8002/optimize/cms-process/{process_id}"
    
    # CMS Authentication token
    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImVtYWlsIjoic3VwZXJhZG1pbkBleGFtcGxlLmNvbSIsInJvbGUiOiJTVVBFUl9BRE1JTiIsIm5hbWUiOiJTdXBlciBBZG1pbiIsImlhdCI6MTc1NzMxNDc2OSwiZXhwIjoxNzU3OTE5NTY5fQ.OLdaZNroqLnbfub-0jRVwZUQZJIyMTegioFGtj2dsEk"
    
    # Headers with authentication
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    
    print("Testing CMS Integration...")
    print(f"Process: {cms_data['process_name']}")
    print(f"Company: {cms_data['company']['name']}")
    print(f"Total Tasks: {len(cms_data['process_tasks'])}")
    print("-" * 50)
    
    try:
        # Send POST request with authentication
        response = requests.post(url, json=cms_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n[SUCCESS] CMS Integration Successful!")
            print("\nProcess Info:")
            print(f"  - Process ID: {result['process_info']['process_id']}")
            print(f"  - Process Name: {result['process_info']['process_name']}")
            print(f"  - Company: {result['process_info']['company']}")
            
            print("\nBaseline Scenario (CMS Process):")
            baseline = result['baseline']
            print(f"  - Duration: {baseline['total_duration_days']:.1f} days")
            print(f"  - Cost: ${baseline['total_cost']:,.2f}")
            print(f"  - Quality Score: {baseline['quality_score']:.2f}")
            
            print("\nOptimized Scenarios:")
            for i, scenario in enumerate(result['scenarios'], 1):
                print(f"\n  Scenario {i}: {scenario['name']}")
                print(f"    - Duration: {scenario['total_duration_days']:.1f} days")
                print(f"    - Cost: ${scenario['total_cost']:,.2f}")
                print(f"    - Quality Score: {scenario['quality_score']:.2f}")
                print(f"    - Optimization Type: {scenario['optimization_type']}")
                
                # Calculate improvements from baseline
                if i > 1:  # Skip baseline itself
                    duration_improvement = (baseline['total_duration_days'] - scenario['total_duration_days']) / baseline['total_duration_days'] * 100
                    cost_difference = (scenario['total_cost'] - baseline['total_cost']) / baseline['total_cost'] * 100
                    
                    if duration_improvement > 0:
                        print(f"    - Time Saved: {duration_improvement:.1f}%")
                    if cost_difference < 0:
                        print(f"    - Cost Saved: {abs(cost_difference):.1f}%")
                    elif cost_difference > 0:
                        print(f"    - Cost Increase: {cost_difference:.1f}%")
            
            # Save results
            with open('cms_optimization_results.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("\n[SAVED] Results saved to cms_optimization_results.json")
            
        else:
            print(f"\n[ERROR] Status Code: {response.status_code}")
            print(response.json())
            
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to API")
        print("Make sure the API server is running on http://localhost:8002")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")

if __name__ == "__main__":
    test_cms_endpoint()

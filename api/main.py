from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.models.data_models import Project
from src.optimization.scenario_generator import ScenarioGenerator
from src.optimization.pareto_optimizer import ParetoOptimizer

app = FastAPI(title="What-If Analysis API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CustomConstraints(BaseModel):
    resources: Dict[str, Dict[str, Any]]
    tasks: Dict[str, Dict[str, Any]]
    preferences: Dict[str, float]

class OptimizeRequest(BaseModel):
    process_name: str
    constraints: Optional[CustomConstraints] = None

# Available processes mapping
PROCESS_FILES = {
    "hospital_project": "example/hospital_project.json",
    "software_project": "example/software_project.json",
    "manufacturing_project": "example/manufacturing_project.json"
}

@app.get("/")
async def root():
    return {"message": "What-If Analysis API is running"}

@app.get("/processes")
async def get_available_processes():
    """Get list of available processes"""
    processes = []
    base_path = Path(__file__).parent.parent
    
    for process_id, file_path in PROCESS_FILES.items():
        full_path = base_path / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r') as f:
                    data = json.load(f)
                processes.append({
                    "id": process_id,
                    "name": data.get("name", process_id),
                    "description": data.get("description", ""),
                    "tasks_count": len(data.get("tasks", [])),
                    "resources_count": len(data.get("resources", []))
                })
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    
    return {"processes": processes}

@app.post("/optimize/custom")
async def optimize_custom(request: OptimizeRequest):
    """Optimize with custom constraints"""
    print(f"DEBUG: Received request for process: {request.process_name}")
    print(f"DEBUG: Available processes: {list(PROCESS_FILES.keys())}")
    if request.process_name not in PROCESS_FILES:
        raise HTTPException(status_code=404, detail=f"Process not found: {request.process_name}")
    
    try:
        # Load base project
        base_path = Path(__file__).parent.parent
        file_path = base_path / PROCESS_FILES[request.process_name]
        
        with open(file_path, 'r') as f:
            project_data = json.load(f)
        
        # Apply custom constraints
        if request.constraints:
            project_data = apply_constraints(project_data, request.constraints)
        
        # Create temporary project with constraints
        project = Project.from_json(project_data)
        
        # Generate optimized scenario based on preferences and constraints
        generator = ScenarioGenerator(project)
        
        # Check if any tasks have parallel execution enabled
        has_parallel_tasks = False
        task_constraints = {}
        if request.constraints and request.constraints.tasks:
            for task_id, constraint in request.constraints.tasks.items():
                task_constraints[task_id] = constraint
                if constraint.get('allow_parallel', False):
                    has_parallel_tasks = True
        
        # Choose optimization type based on preferences
        time_pref = request.constraints.preferences.get('time_priority', 0.33) if request.constraints else 0.33
        cost_pref = request.constraints.preferences.get('cost_priority', 0.33) if request.constraints else 0.33
        quality_pref = request.constraints.preferences.get('quality_priority', 0.34) if request.constraints else 0.34
        
        # Use custom parallel scenario if parallel tasks are configured
        if has_parallel_tasks:
            scenario = generator.generate_custom_parallel_scenario(task_constraints)
        elif time_pref > cost_pref and time_pref > quality_pref:
            scenario = generator.generate_parallel_scenario()
        elif cost_pref > time_pref and cost_pref > quality_pref:
            scenario = generator.generate_cost_optimized_scenario()
        else:
            scenario = generator.generate_balanced_scenario()
        
        # Evaluate scenario
        optimizer = ParetoOptimizer(project)
        metrics = optimizer.evaluate_scenario(scenario)
        
        result = {
            'scenario': scenario.to_dict(),
            'metrics': metrics.to_dict()
        }
        
        return {
            "success": True,
            "scenario": result,
            "project_data": project_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Custom optimization failed: {str(e)}")

@app.post("/optimize/{process_name}")
async def optimize_process(process_name: str):
    """Optimize a process and return the best scenario"""
    if process_name not in PROCESS_FILES:
        raise HTTPException(status_code=404, detail="Process not found")
    
    try:
        # Load project data
        base_path = Path(__file__).parent.parent
        file_path = base_path / PROCESS_FILES[process_name]
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Process file not found")
        
        # Load and parse project
        project = Project.from_json_file(str(file_path))
        
        # Generate scenarios
        generator = ScenarioGenerator(project)
        scenarios = [
            generator.generate_baseline_scenario(),
            generator.generate_parallel_scenario(),
            generator.generate_cost_optimized_scenario(),
            generator.generate_balanced_scenario(),
            generator.generate_critical_path_scenario(),
            generator.generate_resource_leveling_scenario()
        ]
        
        # Find best scenario using Pareto optimization
        optimizer = ParetoOptimizer(project)
        pareto_scenarios = []
        
        for scenario in scenarios:
            metrics = optimizer.evaluate_scenario(scenario)
            pareto_scenarios.append({
                'scenario': scenario.to_dict(),
                'metrics': metrics.to_dict()
            })
        
        # Select best overall scenario (highest overall score)
        best_scenario = max(pareto_scenarios, key=lambda x: x['metrics']['overall_score'])
        
        # Load raw project data for frontend
        with open(file_path, 'r') as f:
            project_data = json.load(f)
        
        return {
            "success": True,
            "best_scenario": best_scenario,
            "project_data": project_data,
            "constraints": extract_constraints(project_data),
            "all_scenarios": pareto_scenarios
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

def extract_constraints(project_data: Dict) -> Dict:
    """Extract current constraints from project data"""
    return {
        "resources": {
            resource["id"]: {
                "hourly_rate": resource["hourly_rate"],
                "max_hours_per_day": resource["max_hours_per_day"],
                "available": True,
                "skills": resource["skills"]
            }
            for resource in project_data["resources"]
        },
        "tasks": {
            task["id"]: {
                "duration_hours": task["duration_hours"],
                "priority": 3,  # Default normal priority
                "allow_parallel": False,
                "required_skills": task["required_skills"],
                "order": task["order"]
            }
            for task in project_data["tasks"]
        },
        "preferences": {
            "time_priority": 0.33,
            "cost_priority": 0.33,
            "quality_priority": 0.34
        }
    }

def apply_constraints(project_data: Dict, constraints: CustomConstraints) -> Dict:
    """Apply custom constraints to project data"""
    # Update resources
    resources_to_remove = []
    for resource in project_data["resources"]:
        resource_id = resource["id"]
        if resource_id in constraints.resources:
            constraint = constraints.resources[resource_id]
            resource["hourly_rate"] = constraint.get("hourly_rate", resource["hourly_rate"])
            resource["max_hours_per_day"] = constraint.get("max_hours_per_day", resource["max_hours_per_day"])
            
            # Mark resource for removal if not available
            if not constraint.get("available", True):
                resources_to_remove.append(resource_id)
    
    # Remove unavailable resources
    project_data["resources"] = [r for r in project_data["resources"] if r["id"] not in resources_to_remove]
    
    # Update tasks with parallel execution logic
    for task in project_data["tasks"]:
        task_id = task["id"]
        if task_id in constraints.tasks:
            constraint = constraints.tasks[task_id]
            task["duration_hours"] = constraint.get("duration_hours", task["duration_hours"])
            
            # Store parallel execution flag for scenario generation
            task["allow_parallel"] = constraint.get("allow_parallel", False)
            task["priority"] = constraint.get("priority", 3)
    
    return project_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

# What-If Analysis Dashboard

A comprehensive project optimization tool with AI-powered resource allocation and interactive constraint adjustment.

## Features

### 🎯 **Core Functionality**
- **Process Selection**: Choose from Hospital, Software, or Manufacturing projects
- **AI Optimization**: Get the best scenario using advanced algorithms
- **Resource Allocation**: Detailed breakdown of task assignments
- **Real-time Impact**: See cost/time changes as you adjust constraints

### 🛠️ **Constraint Adjustment**
- **Resource Controls**: Adjust hourly rates, availability, max hours per day
- **Task Controls**: Modify duration, priority, parallel execution options
- **Optimization Preferences**: Balance time vs cost vs quality priorities

### 📊 **Comparison & Analysis**
- **Scenario Comparison**: Compare custom scenarios with AI-optimized baseline
- **Impact Visualization**: Real-time preview of constraint changes
- **Detailed Metrics**: Duration, cost, quality scores, resource utilization

## Quick Start

### 1. Install Dependencies
```bash
# Install API dependencies
pip install -r api/requirements.txt

# Install main project dependencies
pip install -r requirements.txt
```

### 2. Launch Dashboard
```bash
python run_frontend.py
```

This will:
- Start FastAPI backend on `http://localhost:8000`
- Start frontend server on `http://localhost:3000`
- Open dashboard in your browser automatically

### 3. Use the Dashboard
1. **Select Process**: Choose Hospital, Software, or Manufacturing project
2. **Optimize**: Click "Optimize Process" to get AI-generated best scenario
3. **Adjust Constraints**: Use sliders and controls to modify resources/tasks
4. **Compare**: Enable comparison to see impact of your changes
5. **Reset**: Return to original optimized scenario anytime

## API Endpoints

### `GET /processes`
Get list of available processes to optimize

### `POST /optimize/{process_name}`
Optimize a specific process and return best scenario

### `POST /optimize/custom`
Re-optimize with custom constraints

## Project Structure

```
├── frontend/           # Web dashboard
│   ├── index.html     # Main dashboard interface
│   ├── styles.css     # Modern responsive styling
│   └── script.js      # Interactive functionality
├── api/               # FastAPI backend
│   ├── main.py        # API endpoints and logic
│   └── requirements.txt
├── example/           # Sample projects
│   ├── hospital_project.json
│   ├── software_project.json
│   └── manufacturing_project.json
└── run_frontend.py    # Launch script
```

## Constraint Types

### **Resource Constraints**
- Hourly rates ($30-$200)
- Max hours per day (4-12 hours)
- Resource availability (on/off)

### **Task Constraints**
- Task duration (5-100 hours)
- Task priority (Very Low to Critical)
- Parallel execution allowance

### **Optimization Preferences**
- Time priority (0-100%)
- Cost priority (0-100%)
- Quality priority (0-100%)

## Example Scenarios

### Hospital Project
- 8 tasks from patient intake to hospital-wide rollout
- 8 specialized healthcare resources
- Focus on clinical operations and compliance

### Software Project
- 6 tasks from database design to testing
- 6 developers with different specializations
- Modern e-commerce platform development

### Manufacturing Project
- 5 tasks for smart factory implementation
- 5 engineering specialists
- IoT and automation focus

## Technical Details

- **Backend**: FastAPI with async support
- **Frontend**: Vanilla JavaScript with modern CSS
- **Optimization**: Multiple algorithms (Pareto, RL, heuristic)
- **Real-time Updates**: Live constraint impact calculation
- **Responsive Design**: Works on desktop and mobile

Start exploring different "what-if" scenarios to optimize your projects!

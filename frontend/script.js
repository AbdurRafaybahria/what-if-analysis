// Script updated: 2025-09-07 02:59:46
class WhatIfDashboard {
    constructor() {
        console.log('WhatIfDashboard constructor called - script loaded successfully at 02:59:46');
        this.apiBaseUrl = 'http://localhost:8002';
        this.originalScenario = null;
        this.currentScenario = null;
        this.projectData = null;
        this.constraints = null;
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Process selection
        document.getElementById('processDropdown').addEventListener('change', this.onProcessSelect.bind(this));
        document.getElementById('optimizeBtn').addEventListener('click', this.optimizeProcess.bind(this));
        
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', this.switchTab.bind(this));
        });
        
        // Priority sliders
        ['timePriority', 'costPriority', 'qualityPriority'].forEach(id => {
            document.getElementById(id).addEventListener('input', this.updatePriorities.bind(this));
        });
        
        // Update scenario
        document.getElementById('updateScenarioBtn').addEventListener('click', this.updateScenario.bind(this));
        
        // Comparison controls
        document.getElementById('enableComparisonBtn').addEventListener('click', this.enableComparison.bind(this));
        document.getElementById('resetScenarioBtn').addEventListener('click', this.resetScenario.bind(this));
    }

    onProcessSelect(event) {
        const processValue = event.target.value;
        const optimizeBtn = document.getElementById('optimizeBtn');
        
        if (processValue) {
            optimizeBtn.disabled = false;
        } else {
            optimizeBtn.disabled = true;
        }
    }

    async optimizeProcess() {
        const processName = document.getElementById('processDropdown').value;
        if (!processName) return;

        // Show loading
        document.getElementById('loadingSpinner').classList.remove('hidden');
        document.getElementById('optimizeBtn').disabled = true;

        try {
            // Call API to optimize process
            const response = await fetch(`${this.apiBaseUrl}/optimize/${processName}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            // Store data
            this.originalScenario = result.best_scenario;
            this.currentScenario = { ...result.best_scenario };
            this.projectData = result.project_data;
            this.constraints = result.constraints;

            // Display results
            this.displayBestScenario(result.best_scenario);
            this.setupConstraintControls();
            
            // Initialize impact preview with original scenario metrics
            this.updateImpactPreviewFromScenario(result.best_scenario.metrics);
            
            // Show sections
            document.getElementById('bestScenario').classList.remove('hidden');
            document.getElementById('constraintAdjustment').classList.remove('hidden');
            document.getElementById('comparisonSection').classList.remove('hidden');

        } catch (error) {
            console.error('Error optimizing process:', error);
            alert('Error optimizing process. Please try again.');
        } finally {
            // Hide loading
            document.getElementById('loadingSpinner').classList.add('hidden');
            document.getElementById('optimizeBtn').disabled = false;
        }
    }

    displayBestScenario(scenario) {
        // Update metrics
        document.getElementById('scenarioDuration').textContent = scenario.metrics.total_time_days.toFixed(1);
        document.getElementById('scenarioCost').textContent = `$${scenario.metrics.total_cost.toLocaleString()}`;
        document.getElementById('scenarioQuality').textContent = `${(scenario.metrics.quality_score * 100).toFixed(1)}`;

        // Update allocation table
        const tbody = document.getElementById('allocationBody');
        tbody.innerHTML = '';

        let totalHours = 0;
        let totalCost = 0;

        scenario.scenario.assignments.forEach(assignment => {
            const task = this.projectData.tasks.find(t => t.id === assignment.task_id);
            const resource = this.projectData.resources.find(r => r.id === assignment.resource_id);
            
            const hours = assignment.hours_allocated;
            const cost = hours * resource.hourly_rate;
            totalHours += hours;
            totalCost += cost;

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${task.name}</td>
                <td>${resource.name}</td>
                <td>${hours.toFixed(1)}</td>
                <td>$${cost.toLocaleString()}</td>
                <td>Day ${(assignment.start_time / 8).toFixed(1)}</td>
            `;
            tbody.appendChild(row);
        });

        // Add total row
        const totalRow = document.createElement('tr');
        totalRow.style.fontWeight = 'bold';
        totalRow.style.borderTop = '2px solid #667eea';
        totalRow.innerHTML = `
            <td>TOTAL</td>
            <td>-</td>
            <td>${totalHours.toFixed(1)}</td>
            <td>$${totalCost.toLocaleString()}</td>
            <td>${(totalHours / 8).toFixed(1)} days</td>
        `;
        tbody.appendChild(totalRow);
    }

    setupConstraintControls() {
        this.setupResourceControls();
        this.setupTaskControls();
    }

    setupResourceControls() {
        const container = document.getElementById('resourceControls');
        container.innerHTML = '';

        this.projectData.resources.forEach(resource => {
            const controlGroup = document.createElement('div');
            controlGroup.className = 'control-group';
            controlGroup.innerHTML = `
                <h4>${resource.name}</h4>
                <div class="slider-group">
                    <label>Hourly Rate: $<span id="rate-${resource.id}">${resource.hourly_rate}</span></label>
                    <input type="range" id="rateSlider-${resource.id}" 
                           min="30" max="200" value="${resource.hourly_rate}" 
                           class="slider" data-resource="${resource.id}" data-type="rate">
                </div>
                <div class="slider-group">
                    <label>Max Hours/Day: <span id="hours-${resource.id}">${resource.max_hours_per_day}</span></label>
                    <input type="range" id="hoursSlider-${resource.id}" 
                           min="4" max="12" value="${resource.max_hours_per_day}" 
                           class="slider" data-resource="${resource.id}" data-type="hours">
                </div>
                <div class="checkbox-group">
                    <label>
                        <input type="checkbox" id="available-${resource.id}" checked 
                               data-resource="${resource.id}" data-type="available">
                        Available for assignment
                    </label>
                </div>
            `;
            container.appendChild(controlGroup);

            // Add event listeners
            controlGroup.querySelector(`#rateSlider-${resource.id}`).addEventListener('input', this.onConstraintChange.bind(this));
            controlGroup.querySelector(`#hoursSlider-${resource.id}`).addEventListener('input', this.onConstraintChange.bind(this));
            controlGroup.querySelector(`#available-${resource.id}`).addEventListener('change', this.onConstraintChange.bind(this));
        });
    }

    setupTaskControls() {
        const container = document.getElementById('taskControls');
        container.innerHTML = '';

        this.projectData.tasks.forEach(task => {
            const controlGroup = document.createElement('div');
            controlGroup.className = 'control-group';
            controlGroup.innerHTML = `
                <h4>${task.name}</h4>
                <div class="slider-group">
                    <label>Duration (Hours): <span id="duration-${task.id}">${task.duration_hours}</span></label>
                    <input type="range" id="durationSlider-${task.id}" 
                           min="5" max="100" value="${task.duration_hours}" 
                           class="slider" data-task="${task.id}" data-type="duration">
                </div>
                <div class="slider-group">
                    <label>Priority: <span id="priority-${task.id}">Normal</span></label>
                    <input type="range" id="prioritySlider-${task.id}" 
                           min="1" max="5" value="3" 
                           class="slider" data-task="${task.id}" data-type="priority">
                </div>
                <div class="checkbox-group">
                    <label>
                        <input type="checkbox" id="parallel-${task.id}" 
                               data-task="${task.id}" data-type="parallel">
                        Allow parallel execution
                    </label>
                </div>
            `;
            container.appendChild(controlGroup);

            // Add event listeners
            controlGroup.querySelector(`#durationSlider-${task.id}`).addEventListener('input', this.onConstraintChange.bind(this));
            controlGroup.querySelector(`#prioritySlider-${task.id}`).addEventListener('input', this.onConstraintChange.bind(this));
            
            // Add parallel checkbox event listener with debug
            const parallelCheckbox = controlGroup.querySelector(`#parallel-${task.id}`);
            parallelCheckbox.addEventListener('change', (event) => {
                console.log(`Parallel checkbox changed for task ${task.id}:`, event.target.checked);
                this.onConstraintChange(event);
            });
        });
    }

    onConstraintChange(event) {
        const element = event.target;
        const value = element.type === 'checkbox' ? element.checked : element.value;
        
        console.log(`Constraint changed: ${element.dataset.type} = ${value}`);
        
        // Update display values
        if (element.dataset.type === 'rate') {
            document.getElementById(`rate-${element.dataset.resource}`).textContent = value;
        } else if (element.dataset.type === 'hours') {
            document.getElementById(`hours-${element.dataset.resource}`).textContent = value;
        } else if (element.dataset.type === 'duration') {
            document.getElementById(`duration-${element.dataset.task}`).textContent = value;
        } else if (element.dataset.type === 'priority') {
            const priorities = ['Very Low', 'Low', 'Normal', 'High', 'Critical'];
            document.getElementById(`priority-${element.dataset.task}`).textContent = priorities[value - 1];
        } else if (element.dataset.type === 'parallel') {
            console.log(`Parallel execution changed for task ${element.dataset.task}: ${value}`);
        }

        // Always update impact preview when constraints change
        console.log('Calling updateImpactPreview from onConstraintChange');
        this.updateImpactPreview();
    }

    updatePriorities() {
        const time = document.getElementById('timePriority').value;
        const cost = document.getElementById('costPriority').value;
        const quality = document.getElementById('qualityPriority').value;
        
        // Normalize to 100%
        const total = parseInt(time) + parseInt(cost) + parseInt(quality);
        if (total !== 100) {
            const diff = 100 - total;
            const newQuality = Math.max(0, parseInt(quality) + diff);
            document.getElementById('qualityPriority').value = newQuality;
        }
        
        // Update displays
        document.getElementById('timeValue').textContent = `${time}%`;
        document.getElementById('costValue').textContent = `${cost}%`;
        document.getElementById('qualityValue').textContent = `${document.getElementById('qualityPriority').value}%`;
        
        // Always update impact preview when priorities change
        this.updateImpactPreview();
    }

    updateImpactPreview() {
        console.log('=== updateImpactPreview called ===');
        
        // Check if we have the required data
        if (!this.originalScenario || !this.projectData) {
            console.log('Missing required data - originalScenario or projectData');
            return;
        }
        
        // Calculate estimated impact based on constraint changes
        let estimatedDuration = this.originalScenario.metrics.total_time_days;
        let estimatedCost = this.originalScenario.metrics.total_cost;
        
        console.log('Original duration:', estimatedDuration, 'days');

        // Collect current task configurations
        const taskConfigs = {};
        let hasParallelTasks = false;
        
        this.projectData.tasks.forEach(task => {
            const durationSlider = document.getElementById(`durationSlider-${task.id}`);
            const parallelCheckbox = document.getElementById(`parallel-${task.id}`);
            
            console.log(`Checking task ${task.id}:`);
            console.log('  - Duration slider exists:', !!durationSlider);
            console.log('  - Parallel checkbox exists:', !!parallelCheckbox);
            console.log('  - Parallel checkbox checked:', parallelCheckbox ? parallelCheckbox.checked : 'N/A');
            
            const prioritySlider = document.getElementById(`prioritySlider-${task.id}`);
            const priority = prioritySlider ? parseInt(prioritySlider.value) : 3;
            
            // Apply priority-based duration adjustment
            let baseDuration = durationSlider ? parseFloat(durationSlider.value) : task.duration_hours;
            let priorityAdjustedDuration = this.applyPriorityAdjustment(baseDuration, priority);
            
            taskConfigs[task.id] = {
                originalDuration: task.duration_hours,
                newDuration: priorityAdjustedDuration,
                allowParallel: parallelCheckbox ? parallelCheckbox.checked : false,
                priority: priority,
                order: task.order
            };
            
            console.log(`  - Priority: ${priority}, Base duration: ${baseDuration}h, Adjusted: ${priorityAdjustedDuration}h`);
            
            if (parallelCheckbox && parallelCheckbox.checked) {
                hasParallelTasks = true;
                console.log(`  - Task ${task.id} marked for parallel execution`);
            }
        });

        // Debug: Log task configurations
        console.log('Task configurations:', taskConfigs);
        console.log('Has parallel tasks:', hasParallelTasks);
        
        // Calculate duration considering parallel execution
        if (hasParallelTasks) {
            console.log('Has parallel tasks - using parallel calculation');
            estimatedDuration = this.calculateParallelDuration(taskConfigs);
        } else {
            console.log('No parallel tasks - using sequential calculation');
            // Sequential execution - sum all task durations
            let totalTaskHours = 0;
            Object.values(taskConfigs).forEach(config => {
                totalTaskHours += config.newDuration;
            });
            estimatedDuration = totalTaskHours / 8; // Convert to days
            console.log(`Sequential total: ${totalTaskHours} hours = ${estimatedDuration.toFixed(1)} days`);
        }

        // Calculate priority-adjusted cost
        let priorityAdjustedCost = this.calculatePriorityAdjustedCost(taskConfigs);
        estimatedCost = priorityAdjustedCost;
        
        // Apply resource rate and availability changes to cost
        let costMultiplier = 1.0;
        let durationMultiplier = 1.0;
        
        this.projectData.resources.forEach(resource => {
            const rateSlider = document.getElementById(`rateSlider-${resource.id}`);
            const hoursSlider = document.getElementById(`hoursSlider-${resource.id}`);
            const availableCheckbox = document.getElementById(`available-${resource.id}`);
            
            if (rateSlider && hoursSlider && availableCheckbox) {
                const rateMultiplier = rateSlider.value / resource.hourly_rate;
                const hoursMultiplier = hoursSlider.value / resource.max_hours_per_day;
                const isAvailable = availableCheckbox.checked;
                
                if (isAvailable) {
                    costMultiplier *= rateMultiplier;
                    durationMultiplier *= (1 / hoursMultiplier); // More hours per day = less total duration
                }
            }
        });
        
        estimatedCost *= costMultiplier;
        estimatedDuration *= durationMultiplier;

        // Update display
        console.log('Final estimated duration:', estimatedDuration.toFixed(1), 'days');
        console.log('Final estimated cost:', estimatedCost.toLocaleString());
        
        document.getElementById('impactDuration').textContent = `${estimatedDuration.toFixed(1)} days`;
        document.getElementById('impactCost').textContent = `$${estimatedCost.toLocaleString()}`;
        
        console.log('=== updateImpactPreview completed ===');
    }
    
    calculateParallelDuration(taskConfigs) {
        // Separate parallel and sequential tasks
        const parallelTasks = [];
        const sequentialTasks = [];
        
        Object.entries(taskConfigs).forEach(([taskId, config]) => {
            if (config.allowParallel) {
                parallelTasks.push(config);
            } else {
                sequentialTasks.push(config);
            }
        });
        
        let totalDuration = 0;
        
        // If we have parallel tasks, they can run simultaneously
        if (parallelTasks.length > 0) {
            // Parallel tasks: duration is the maximum of all parallel tasks
            const maxParallelDuration = Math.max(...parallelTasks.map(task => task.newDuration));
            totalDuration += maxParallelDuration;
            
            console.log(`Parallel tasks (${parallelTasks.length}): max duration = ${maxParallelDuration} hours`);
        }
        
        // Sequential tasks are added to the total duration
        if (sequentialTasks.length > 0) {
            const sequentialDuration = sequentialTasks.reduce((sum, task) => sum + task.newDuration, 0);
            totalDuration += sequentialDuration;
            
            console.log(`Sequential tasks (${sequentialTasks.length}): total duration = ${sequentialDuration} hours`);
        }
        
        console.log(`Total calculated duration: ${totalDuration} hours = ${(totalDuration / 8).toFixed(1)} days`);
        
        return totalDuration / 8; // Convert hours to days
    }
    
    applyPriorityAdjustment(baseDuration, priority) {
        // Priority affects resource allocation efficiency
        // Higher priority = better resources = faster completion
        const priorityMultipliers = {
            1: 1.3,   // Very Low - 30% slower (gets junior resources)
            2: 1.15,  // Low - 15% slower
            3: 1.0,   // Normal - baseline
            4: 0.85,  // High - 15% faster (gets senior resources)
            5: 0.7    // Critical - 30% faster (gets best resources)
        };
        
        const multiplier = priorityMultipliers[priority] || 1.0;
        return baseDuration * multiplier;
    }
    
    calculatePriorityAdjustedCost(taskConfigs) {
        // Calculate cost based on priority-adjusted durations and resource rates
        let totalCost = 0;
        
        Object.entries(taskConfigs).forEach(([taskId, config]) => {
            // Find the task in project data to get original cost calculation
            const task = this.projectData.tasks.find(t => t.id === taskId);
            if (!task) return;
            
            // Priority affects which resource tier gets assigned
            const priorityCostMultipliers = {
                1: 0.7,   // Very Low - gets cheapest resources (junior)
                2: 0.85,  // Low - gets lower-cost resources
                3: 1.0,   // Normal - baseline resource cost
                4: 1.25,  // High - gets expensive resources (senior)
                5: 1.5    // Critical - gets most expensive resources (expert)
            };
            
            const baseCostPerHour = 85; // Average hourly rate from original scenario
            const priorityMultiplier = priorityCostMultipliers[config.priority] || 1.0;
            const adjustedRate = baseCostPerHour * priorityMultiplier;
            
            const taskCost = config.newDuration * adjustedRate;
            totalCost += taskCost;
            
            console.log(`Task ${taskId}: Priority ${config.priority}, Duration ${config.newDuration}h, Rate $${adjustedRate}/h, Cost $${taskCost}`);
        });
        
        console.log(`Total priority-adjusted cost: $${totalCost}`);
        return totalCost;
    }
    
    updateImpactPreviewFromScenario(metrics) {
        // Update impact preview with actual scenario metrics
        document.getElementById('impactDuration').textContent = `${metrics.total_time_days.toFixed(1)} days`;
        document.getElementById('impactCost').textContent = `$${metrics.total_cost.toLocaleString()}`;
    }

    async updateScenario() {
        // Get current Impact Preview values to preserve them
        const impactDurationText = document.getElementById('impactDuration').textContent;
        const impactCostText = document.getElementById('impactCost').textContent;
        
        // Parse the values
        const estimatedDuration = parseFloat(impactDurationText.replace(' days', ''));
        const estimatedCost = parseFloat(impactCostText.replace('$', '').replace(/,/g, ''));
        
        // Collect current constraint values
        const updatedConstraints = this.collectConstraints();
        
        try {
            // Call API to re-optimize with new constraints
            const response = await fetch(`${this.apiBaseUrl}/optimize/custom`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    process_name: document.getElementById('processDropdown').value,
                    constraints: updatedConstraints
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            // Create a custom scenario that matches the Impact Preview estimates
            const customScenario = {
                scenario: result.scenario.scenario,
                metrics: {
                    total_time_days: estimatedDuration,
                    total_cost: estimatedCost,
                    quality_score: result.scenario.metrics.quality_score,
                    resource_utilization: result.scenario.metrics.resource_utilization
                }
            };
            
            this.currentScenario = customScenario;
            this.displayBestScenario(customScenario);
            
            // Keep Impact Preview values unchanged since they should match
            
        } catch (error) {
            console.error('Error updating scenario:', error);
            alert('Error updating scenario. Please try again.');
        }
    }

    collectConstraints() {
        const constraints = {
            resources: {},
            tasks: {},
            preferences: {
                time_priority: parseInt(document.getElementById('timePriority').value) / 100,
                cost_priority: parseInt(document.getElementById('costPriority').value) / 100,
                quality_priority: parseInt(document.getElementById('qualityPriority').value) / 100
            }
        };

        // Collect resource constraints
        this.projectData.resources.forEach(resource => {
            constraints.resources[resource.id] = {
                hourly_rate: parseFloat(document.getElementById(`rateSlider-${resource.id}`).value),
                max_hours_per_day: parseFloat(document.getElementById(`hoursSlider-${resource.id}`).value),
                available: document.getElementById(`available-${resource.id}`).checked
            };
        });

        // Collect task constraints
        this.projectData.tasks.forEach(task => {
            constraints.tasks[task.id] = {
                duration_hours: parseFloat(document.getElementById(`durationSlider-${task.id}`).value),
                priority: parseInt(document.getElementById(`prioritySlider-${task.id}`).value),
                allow_parallel: document.getElementById(`parallel-${task.id}`).checked
            };
        });

        return constraints;
    }

    switchTab(event) {
        const targetTab = event.target.dataset.tab;
        
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        document.getElementById(`${targetTab}Tab`).classList.add('active');
    }

    enableComparison() {
        if (!this.originalScenario || !this.currentScenario) return;

        const comparisonTable = document.getElementById('comparisonTable');
        const tbody = document.getElementById('comparisonBody');
        
        tbody.innerHTML = '';

        // Compare metrics
        const metrics = [
            { label: 'Duration (days)', original: this.originalScenario.metrics.total_time_days, current: this.currentScenario.metrics.total_time_days },
            { label: 'Total Cost', original: this.originalScenario.metrics.total_cost, current: this.currentScenario.metrics.total_cost },
            { label: 'Quality Score', original: this.originalScenario.metrics.quality_score * 100, current: this.currentScenario.metrics.quality_score * 100 },
            { label: 'Resource Utilization', original: this.originalScenario.metrics.resource_utilization * 100, current: this.currentScenario.metrics.resource_utilization * 100 }
        ];

        metrics.forEach(metric => {
            const difference = metric.current - metric.original;
            const percentChange = ((difference / metric.original) * 100).toFixed(1);
            
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${metric.label}</td>
                <td>${metric.label.includes('Cost') ? '$' : ''}${metric.original.toFixed(1)}${metric.label.includes('Score') || metric.label.includes('Utilization') ? '%' : ''}</td>
                <td>${metric.label.includes('Cost') ? '$' : ''}${metric.current.toFixed(1)}${metric.label.includes('Score') || metric.label.includes('Utilization') ? '%' : ''}</td>
                <td class="${difference >= 0 ? 'difference-positive' : 'difference-negative'}">
                    ${difference >= 0 ? '+' : ''}${difference.toFixed(1)} (${percentChange}%)
                </td>
            `;
            tbody.appendChild(row);
        });

        comparisonTable.classList.remove('hidden');
    }

    resetScenario() {
        if (!this.originalScenario) return;
        
        this.currentScenario = { ...this.originalScenario };
        this.displayBestScenario(this.originalScenario);
        
        // Reset impact preview to original scenario metrics
        this.updateImpactPreviewFromScenario(this.originalScenario.metrics);
        
        // Reset all controls to original values
        this.projectData.resources.forEach(resource => {
            document.getElementById(`rateSlider-${resource.id}`).value = resource.hourly_rate;
            document.getElementById(`hoursSlider-${resource.id}`).value = resource.max_hours_per_day;
            document.getElementById(`available-${resource.id}`).checked = true;
            document.getElementById(`rate-${resource.id}`).textContent = resource.hourly_rate;
            document.getElementById(`hours-${resource.id}`).textContent = resource.max_hours_per_day;
        });

        this.projectData.tasks.forEach(task => {
            document.getElementById(`durationSlider-${task.id}`).value = task.duration_hours;
            document.getElementById(`prioritySlider-${task.id}`).value = 3;
            document.getElementById(`parallel-${task.id}`).checked = false;
            document.getElementById(`duration-${task.id}`).textContent = task.duration_hours;
            document.getElementById(`priority-${task.id}`).textContent = 'Normal';
        });

        // Reset priorities
        document.getElementById('timePriority').value = 33;
        document.getElementById('costPriority').value = 33;
        document.getElementById('qualityPriority').value = 34;
        this.updatePriorities();

        // Hide comparison
        document.getElementById('comparisonTable').classList.add('hidden');
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    new WhatIfDashboard();
});

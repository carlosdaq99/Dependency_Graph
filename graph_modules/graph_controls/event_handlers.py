"""
Event Handlers Module
====================

Event handling and state management for graph controls.
Handles user interactions, filter changes, and layout switching events.
"""


def get_event_handlers_js() -> str:
    """
    Get JavaScript code for event handling and state management.

    Returns:
        str: JavaScript code for event handlers and interactions
    """
    return """
        function toggleFolder(folder) {
            if (checkedFolders.has(folder)) {
                checkedFolders.delete(folder);
            } else {
                checkedFolders.add(folder);
            }
            updateEnhancedControls();
            updateEnhancedVisibility();
            updateEnhancedStats();
            
            // If in force layout, restart simulation to reposition visible nodes
            if (currentLayout === "force" && typeof restartForceSimulation === "function") {
                restartForceSimulation();
            }
        }
        
        function toggleTestDependencies() {
            showTestDependencies = !showTestDependencies;
            updateEnhancedControls();
            updateEnhancedVisibility();
            updateEnhancedStats();
            
            // If in force layout, restart simulation to reposition visible nodes
            if (currentLayout === "force" && typeof restartForceSimulation === "function") {
                restartForceSimulation();
            }
        }
        
        function togglePathHighlighting() {
            showCompletePaths = !showCompletePaths;
            updateEnhancedControls();
            
            // Re-apply highlighting if a node is currently selected
            if (selectedNode) {
                highlightEnhancedDirectPath(selectedNode);
            }
        }
        
        function resetAllFilters() {
            checkedFolders = new Set(Object.keys(graphData.subfolder_info));
            showTestDependencies = true;
            
            // Reset range filters to project-based maximum values
            predecessorsRangeFilter = { min: 0, max: {max_pred} };
            successorsRangeFilter = { min: 0, max: {max_succ} };
            sizeRangeFilter = { min: 0, max: {max_size} };
            
            // Update UI controls for range filters
            document.getElementById('predecessors-min-filter').value = predecessorsRangeFilter.min;
            document.getElementById('predecessors-max-filter').value = predecessorsRangeFilter.max;
            document.getElementById('successors-min-filter').value = successorsRangeFilter.min;
            document.getElementById('successors-max-filter').value = successorsRangeFilter.max;
            document.getElementById('size-min-filter').value = sizeRangeFilter.min;
            document.getElementById('size-max-filter').value = sizeRangeFilter.max;
            updateFilterLabels();
            
            resetHighlighting();
            updateEnhancedControls();
            updateEnhancedVisibility();
            updateEnhancedStats();
        }

        function setupAdvancedFilters() {
            // Predecessors range filters
            const predecessorsMinSlider = document.getElementById('predecessors-min-filter');
            const predecessorsMaxSlider = document.getElementById('predecessors-max-filter');
            
            predecessorsMinSlider.addEventListener('input', function() {
                predecessorsRangeFilter.min = parseInt(this.value);
                if (predecessorsRangeFilter.min > predecessorsRangeFilter.max) {
                    predecessorsRangeFilter.max = predecessorsRangeFilter.min;
                    predecessorsMaxSlider.value = predecessorsRangeFilter.max;
                }
                updateFilterLabels();
                updateEnhancedVisibility();
                updateEnhancedStats();
            });
            
            predecessorsMaxSlider.addEventListener('input', function() {
                predecessorsRangeFilter.max = parseInt(this.value);
                if (predecessorsRangeFilter.max < predecessorsRangeFilter.min) {
                    predecessorsRangeFilter.min = predecessorsRangeFilter.max;
                    predecessorsMinSlider.value = predecessorsRangeFilter.min;
                }
                updateFilterLabels();
                updateEnhancedVisibility();
                updateEnhancedStats();
            });
            
            // Successors range filters
            const successorsMinSlider = document.getElementById('successors-min-filter');
            const successorsMaxSlider = document.getElementById('successors-max-filter');
            
            successorsMinSlider.addEventListener('input', function() {
                successorsRangeFilter.min = parseInt(this.value);
                if (successorsRangeFilter.min > successorsRangeFilter.max) {
                    successorsRangeFilter.max = successorsRangeFilter.min;
                    successorsMaxSlider.value = successorsRangeFilter.max;
                }
                updateFilterLabels();
                updateEnhancedVisibility();
                updateEnhancedStats();
            });
            
            successorsMaxSlider.addEventListener('input', function() {
                successorsRangeFilter.max = parseInt(this.value);
                if (successorsRangeFilter.max < successorsRangeFilter.min) {
                    successorsRangeFilter.min = successorsRangeFilter.max;
                    successorsMinSlider.value = successorsRangeFilter.min;
                }
                updateFilterLabels();
                updateEnhancedVisibility();
                updateEnhancedStats();
            });
            
            // Size range filters
            const sizeMinSlider = document.getElementById('size-min-filter');
            const sizeMaxSlider = document.getElementById('size-max-filter');
            
            sizeMinSlider.addEventListener('input', function() {
                sizeRangeFilter.min = parseInt(this.value);
                if (sizeRangeFilter.min > sizeRangeFilter.max) {
                    sizeRangeFilter.max = sizeRangeFilter.min;
                    sizeMaxSlider.value = sizeRangeFilter.max;
                }
                updateFilterLabels();
                updateEnhancedVisibility();
                updateEnhancedStats();
            });
            
            sizeMaxSlider.addEventListener('input', function() {
                sizeRangeFilter.max = parseInt(this.value);
                if (sizeRangeFilter.max < sizeRangeFilter.min) {
                    sizeRangeFilter.min = sizeRangeFilter.max;
                    sizeMinSlider.value = sizeRangeFilter.min;
                }
                updateFilterLabels();
                updateEnhancedVisibility();
                updateEnhancedStats();
            });
            
            // Select all toggle
            const selectAllToggle = document.getElementById('select-all-toggle');
            selectAllToggle.addEventListener('click', function() {
                const allFolders = Object.keys(graphData.subfolder_info);
                const allSelected = allFolders.every(folder => checkedFolders.has(folder));
                
                if (allSelected) {
                    checkedFolders.clear();
                } else {
                    checkedFolders = new Set(allFolders);
                }
                
                updateEnhancedControls();
                updateEnhancedVisibility();
                updateEnhancedStats();
            });
            
            updateFilterLabels();
        }

        // Setup layout toggle functionality
        function setupLayoutToggle() {
            const toggleSwitch = document.getElementById('toggle-switch');
            const layoutToggle = document.getElementById('layout-toggle');
            
            if (!toggleSwitch) {
                console.error("❌ Toggle switch element not found!");
                return;
            }
            
            if (!layoutToggle) {
                console.error("❌ Layout toggle element not found!");
                return;
            }
            
            console.log("🎮 Setting up layout toggle event listeners...");
            
            function handleToggle() {
                console.log("🖱️ Toggle clicked! Current layout:", currentLayout);
                const newLayout = currentLayout === "hierarchical" ? "force" : "hierarchical";
                switchLayout(newLayout);
            }
            
            toggleSwitch.addEventListener('click', function(event) {
                console.log("🎯 Toggle switch clicked directly");
                handleToggle();
            });
            
            layoutToggle.addEventListener('click', function(event) {
                console.log("🎯 Layout toggle area clicked, target:", event.target.className);
                if (event.target === toggleSwitch || event.target.closest('.toggle-switch')) {
                    console.log("   → Click on toggle switch itself, letting it handle");
                    return; // Let the toggle switch handle it
                }
                console.log("   → Click outside toggle switch, handling toggle");
                handleToggle();
            });
            
            // Keyboard accessibility
            toggleSwitch.addEventListener('keydown', function(event) {
                if (event.key === 'Enter' || event.key === ' ') {
                    console.log("⌨️ Toggle activated via keyboard:", event.key);
                    event.preventDefault();
                    handleToggle();
                }
            });
            
            toggleSwitch.setAttribute('tabindex', '0');
            toggleSwitch.setAttribute('role', 'switch');
            toggleSwitch.setAttribute('aria-checked', 'false');
            
            console.log("✅ Layout toggle setup complete");
        }

        // Initialize all controls functionality
        function initializeControls() {
            console.log("🎮 Initializing UI controls...");
            
            // Setup all control functionalities
            setupAdvancedFilters();
            setupLayoutToggle();
            setupSearchFunctionality();
            setupPerformanceMonitoring();
            
            console.log("✅ All UI controls initialized successfully");
        }
        
        // Expose initialization function globally
        window.initializeControls = initializeControls;
    """

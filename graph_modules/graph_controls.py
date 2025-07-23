"""
Graph Controls Module
====================

JavaScript UI controls, event handling, and filter management.
Handles layout switching, folder toggles, advanced filters, and statistics.
"""


def get_graph_controls_js() -> str:
    """
    Get JavaScript code for UI controls and event handling.

    Returns:
        str: JavaScript code for controls and interaction
    """
    return """
        // Theme management
        let currentTheme = localStorage.getItem('dependency-graph-theme') || 'light';
        
        function initializeTheme() {
            document.documentElement.setAttribute('data-theme', currentTheme);
            updateThemeToggle();
        }
        
        function toggleTheme() {
            currentTheme = currentTheme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', currentTheme);
            localStorage.setItem('dependency-graph-theme', currentTheme);
            updateThemeToggle();
            
            // Update node and link colors for the current theme
            if (typeof updateVisualizationForTheme === 'function') {
                updateVisualizationForTheme();
            }
        }
        
        function updateThemeToggle() {
            const toggle = document.querySelector('.theme-toggle');
            if (toggle) {
                const icon = toggle.querySelector('.theme-icon');
                const text = toggle.querySelector('.theme-text');
                if (currentTheme === 'dark') {
                    icon.textContent = '☀️';
                    text.textContent = 'Light';
                } else {
                    icon.textContent = '🌙';
                    text.textContent = 'Dark';
                }
            }
        }
        
        // Enhanced controls management
        function updateEnhancedControls() {
            const container = d3.select("#folder-controls");
            container.selectAll("*").remove();
            
            Object.entries(graphData.subfolder_info)
                .sort((a, b) => Number(b[1].count) - Number(a[1].count))
                .forEach(([folder, info]) => {
                const item = container.append("div")
                    .attr("class", "folder-item")
                    .attr("role", "checkbox")
                    .attr("aria-checked", checkedFolders.has(folder))
                    .attr("tabindex", "0")
                    .on("click", () => toggleFolder(folder))
                    .on("keydown", function(event) {
                        if (event.key === "Enter" || event.key === " ") {
                            event.preventDefault();
                            toggleFolder(folder);
                        }
                    });
                
                item.append("span")
                    .attr("class", "folder-checkbox")
                    .text(checkedFolders.has(folder) ? "☑" : "☐");
                
                item.append("div")
                    .attr("class", "folder-color")
                    .style("background-color", info.color);
                
                const labelText = `${folder} <span class="folder-count">(${info.count} modules)</span>`;
                const testText = info.test_modules && info.test_modules.length > 0 ? 
                    ` <span class="test-count">[${info.test_modules.length} tests]</span>` : "";
                
                item.append("span")
                    .attr("class", "folder-label")
                    .html(labelText + testText);
            });
            
            // Test toggle
            const testToggle = d3.select("#test-toggle");
            testToggle.select(".folder-checkbox")
                .text(showTestDependencies ? "☑" : "☐");
            
            testToggle.on("click", toggleTestDependencies);
            
            // Path highlighting toggle
            const pathToggle = d3.select("#path-highlighting-toggle");
            pathToggle.select(".folder-checkbox")
                .text(showCompletePaths ? "☑" : "☐");
            
            pathToggle.on("click", togglePathHighlighting);
            
            // Update "Select All" toggle
            const allFolders = Object.keys(graphData.subfolder_info);
            const allSelected = allFolders.every(folder => checkedFolders.has(folder));
            const selectAllToggle = d3.select("#select-all-toggle");
            selectAllToggle.select(".folder-checkbox")
                .text(allSelected ? "☑" : "☐");
        }
        
        function updateEnhancedStats() {
            const visibleNodes = graphData.nodes.filter(n => shouldShowNode(n));
            const visibleEdges = graphData.edges.filter(e => shouldShowEdge(e));
            const testFiles = visibleNodes.filter(n => n.is_test).length;
            
            const stats = [
                { value: graphData.nodes.length, label: "Total Files" },
                { value: visibleNodes.length, label: "Visible Files" },
                { value: graphData.edges.length, label: "Edges" },
                { value: visibleEdges.length, label: "Visible Edges" },
                { value: Object.keys(graphData.subfolder_info).length, label: "Directories" },
                { value: testFiles, label: "Test Files" }
            ];
            
            const container = d3.select("#stats-content");
            container.selectAll("*").remove();
            
            stats.forEach(stat => {
                const item = container.append("div").attr("class", "stat-item");
                item.append("div").attr("class", "stat-value").text(stat.value);
                item.append("div").attr("class", "stat-label").text(stat.label);
            });
        }
        
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
        
        // Advanced filter functions
        function updateFilterLabels() {
            document.getElementById('predecessors-filter-value').textContent = 
                `${predecessorsRangeFilter.min} - ${predecessorsRangeFilter.max}`;
            document.getElementById('successors-filter-value').textContent = 
                `${successorsRangeFilter.min} - ${successorsRangeFilter.max}`;
            document.getElementById('size-filter-value').textContent = 
                `${sizeRangeFilter.min} - ${sizeRangeFilter.max}`;
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
        
        // Switch between hierarchical and force-directed layouts
        function switchLayout(newLayout) {
            if (newLayout === currentLayout) return;
            
            console.log(`🔄 Switching from ${currentLayout} to ${newLayout} layout`);
            currentLayout = newLayout;
            
            // Update toggle UI
            const toggleSwitch = document.getElementById('toggle-switch');
            const layoutIndicator = document.getElementById('layout-indicator');
            
            if (newLayout === "force") {
                toggleSwitch.classList.add('active');
                layoutIndicator.textContent = "Current: Force-Directed Layout";
                
                console.log("🔄 DEBUG: Switching to force layout");
                
                // Use the simplified container switching approach
                if (typeof window.switchToLayout === 'function') {
                    window.switchToLayout("force");
                } else {
                    console.error("❌ switchToLayout function not available!");
                }
                
            } else {
                toggleSwitch.classList.remove('active');
                layoutIndicator.textContent = "Current: Hierarchical Layout";
                
                console.log("🔄 DEBUG: Switching to hierarchical layout");
                
                // Use the simplified container switching approach
                if (typeof window.switchToLayout === 'function') {
                    window.switchToLayout("hierarchical");
                } else {
                    console.error("❌ switchToLayout function not available!");
                }
            }
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
        
        // Search functionality
        function setupSearchFunctionality() {
            const searchInput = document.getElementById('search-input');
            if (!searchInput) return;
            
            searchInput.addEventListener('input', function() {
                const query = this.value.toLowerCase().trim();
                
                if (query === '') {
                    resetHighlighting();
                    return;
                }
                
                // Find matching nodes
                const matchingNodes = graphData.nodes.filter(node => 
                    node.stem.toLowerCase().includes(query) ||
                    node.folder.toLowerCase().includes(query) ||
                    node.name.toLowerCase().includes(query)
                );
                
                if (matchingNodes.length > 0) {
                    // Highlight matching nodes
                    const matchingIds = new Set(matchingNodes.map(n => n.id));
                    
                    window.graphElements.node
                        .classed("highlighted", d => matchingIds.has(d.id))
                        .classed("dimmed", d => !matchingIds.has(d.id));
                    
                    window.graphElements.node.selectAll(".node-rect, .node-circle")
                        .classed("highlighted", function() {
                            const nodeData = d3.select(this.parentNode).datum();
                            return matchingIds.has(nodeData.id);
                        })
                        .classed("dimmed", function() {
                            const nodeData = d3.select(this.parentNode).datum();
                            return !matchingIds.has(nodeData.id);
                        });
                    
                    window.graphElements.link.classed("dimmed", true);
                }
            });
        }
        
        // Performance monitoring
        function setupPerformanceMonitoring() {
            let frameCount = 0;
            let lastTime = performance.now();
            
            function updateFPS() {
                const now = performance.now();
                frameCount++;
                
                if (now - lastTime >= 1000) {
                    const fps = Math.round(frameCount * 1000 / (now - lastTime));
                    const fpsElement = document.getElementById('fps-counter');
                    if (fpsElement) {
                        fpsElement.textContent = `FPS: ${fps}`;
                    }
                    
                    frameCount = 0;
                    lastTime = now;
                }
                
                requestAnimationFrame(updateFPS);
            }
            
            updateFPS();
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

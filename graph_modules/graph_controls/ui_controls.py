"""
UI Controls Module
=================

UI control generation, layout management, and visual interface components.
Handles theme management, folder controls, statistics display, and search functionality.
"""


def get_ui_controls_js() -> str:
    """
    Get JavaScript code for UI control generation and management.

    Returns:
        str: JavaScript code for UI controls and layout
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
        
        // === Configurable Control Panel Section Order ===
        // Change this array to reorder control panel cards
        const controlPanelOrder = [
            'statistics',
            'layoutControls', 
            'directories',
            'testControls',
            'highlightingOptions',
            'advancedFilters'
        ];

        // Mapping from card name to render function
        const controlPanelRenderers = {
            statistics: updateStatisticsCard,
            layoutControls: updateLayoutControlsCard,
            directories: updateDirectoriesCard,
            testControls: updateTestControlsCard,
            highlightingOptions: updateHighlightingOptionsCard,
            advancedFilters: updateAdvancedFiltersCard
        };

        // Main render function for control panel
        function renderControlPanel() {
            controlPanelOrder.forEach(cardName => {
                if (controlPanelRenderers[cardName]) {
                    controlPanelRenderers[cardName]();
                }
            });
        }

        // === Individual Card Renderers ===
        
        // Statistics Card
        function updateStatisticsCard() {
            // Updates #stats-content container
            updateEnhancedStats();
        }

        // Layout Controls Card (includes layout toggle + path highlighting)
        function updateLayoutControlsCard() {
            // Update layout toggle
            const toggleSwitch = document.getElementById('toggle-switch');
            const layoutIndicator = document.getElementById('layout-indicator');
            
            if (toggleSwitch) {
                if (currentLayout === "force") {
                    toggleSwitch.classList.add('active');
                    layoutIndicator.textContent = "Current: Force-Directed Layout";
                } else {
                    toggleSwitch.classList.remove('active');
                    layoutIndicator.textContent = "Current: Hierarchical Layout";
                }
            }

            // Update path highlighting toggle (moved from highlighting options)
            const pathToggle = d3.select("#path-highlighting-toggle");
            pathToggle.select(".folder-checkbox")
                .text(showCompletePaths ? "☑" : "☐");
            pathToggle.on("click", togglePathHighlighting);
        }

        // Directories Card  
        function updateDirectoriesCard() {
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
            
            // Update "Select All" toggle
            const allFolders = Object.keys(graphData.subfolder_info);
            const allSelected = allFolders.every(folder => checkedFolders.has(folder));
            const selectAllToggle = d3.select("#select-all-toggle");
            selectAllToggle.select(".folder-checkbox")
                .text(allSelected ? "☑" : "☐");
        }

        // Test Controls Card
        function updateTestControlsCard() {
            const testToggle = d3.select("#test-toggle");
            testToggle.select(".folder-checkbox")
                .text(showTestDependencies ? "☑" : "☐");
            testToggle.on("click", toggleTestDependencies);
        }

        // Highlighting Options Card
        function updateHighlightingOptionsCard() {
            // Reserved for future highlighting options
            // Path highlighting moved to Layout Controls
        }

        // Advanced Filters Card
        function updateAdvancedFiltersCard() {
            // Updates advanced filter controls if they exist
            if (typeof updateFilterLabels === 'function') {
                updateFilterLabels();
            }
        }

        // Legacy function - now calls the new system
        function updateEnhancedControls() {
            renderControlPanel();
        }
        
        function updateEnhancedStats() {
            const visibleNodes = graphData.nodes.filter(n => shouldShowNode(n));
            const visibleEdges = graphData.edges.filter(e => shouldShowEdge(e));
            const testFiles = visibleNodes.filter(n => n.is_test).length;
            
            // Calculate new metrics
            const totalFiles = graphData.nodes.length;
            const directories = Object.keys(graphData.subfolder_info).length;
            
            // Calculate average SLOC (total_lines)
            const nodesWithSLOC = visibleNodes.filter(n => n.total_lines && n.total_lines > 0);
            const avgSLOC = nodesWithSLOC.length > 0 
                ? Math.round(nodesWithSLOC.reduce((sum, n) => sum + n.total_lines, 0) / nodesWithSLOC.length)
                : 0;
            
            // Calculate average performance metric
            const nodesWithPerf = visibleNodes.filter(n => n.performance_score !== undefined);
            const avgPerformance = nodesWithPerf.length > 0 
                ? (nodesWithPerf.reduce((sum, n) => sum + n.performance_score, 0) / nodesWithPerf.length * 100).toFixed(1)
                : "0.0";
            
            // Calculate average file size (convert bytes to KB)
            const nodesWithSize = visibleNodes.filter(n => n.size && n.size > 0);
            const avgFileSize = nodesWithSize.length > 0 
                ? (nodesWithSize.reduce((sum, n) => sum + n.size, 0) / nodesWithSize.length / 1024).toFixed(1)
                : "0.0";
            
            const stats = [
                { value: avgSLOC, label: "Average SLOC" },
                { value: `${avgPerformance}%`, label: "Average Performance" },
                { value: `${avgFileSize} KB`, label: "Average File Size" },
                { value: totalFiles, label: "Total Files" },
                { value: directories, label: "Directories" },
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

        // Advanced filter functions
        function updateFilterLabels() {
            document.getElementById('predecessors-filter-value').textContent = 
                `${predecessorsRangeFilter.min} - ${predecessorsRangeFilter.max}`;
            document.getElementById('successors-filter-value').textContent = 
                `${successorsRangeFilter.min} - ${successorsRangeFilter.max}`;
            document.getElementById('size-filter-value').textContent = 
                `${sizeRangeFilter.min} - ${sizeRangeFilter.max}`;
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
    """

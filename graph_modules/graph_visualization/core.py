"""
Graph Visualization Core Module
==============================

Core initialization, state management, and basic setup for graph visualization.
Contains fundamental D3.js setup, dimension management, and global state variables.
"""


def get_core_visualization_js() -> str:
    """
    Get JavaScript code for core visualization setup and state management.

    Returns:
        str: JavaScript code for core visualization functionality
    """
    return """
        // Enhanced state management
        let checkedFolders = new Set(Object.keys(graphData.subfolder_info));
        let showTestDependencies = true;
        let selectedNode = null;
        let highlightedNodes = new Set();
        let showCompletePaths = false; // New toggle for complete path highlighting

        // Layout state management - SIMPLIFIED APPROACH
        let currentLayout = "hierarchical";
        let simulation = null;
        let hierarchicalContainer = null;
        let forceDirectedContainer = null;

        // Advanced filter state - now using ranges instead of max values
        let predecessorsRangeFilter = { min: 0, max: 20 };
        let successorsRangeFilter = { min: 0, max: 20 };
        let sizeRangeFilter = { min: 0, max: 100 }; // KB

        // D3.js setup with enhanced features
        const svg = d3.select("#graph");
        const tooltip = d3.select("#tooltip");
        let width, height;

        function updateDimensions() {
            const container = document.querySelector('.graph-container');
            width = container.clientWidth;
            height = container.clientHeight;
            svg.attr("width", width).attr("height", height);
        }

        // Initialize enhanced visualization
        function initializeEnhancedVisualization() {
            console.log("🚀 Initializing enhanced dependency graph visualization...");
            
            updateDimensions();
            svg.selectAll("*").remove();
            
            const g = svg.append("g").attr("id", "main-group");
            
            // Setup zoom behavior
            const zoom = d3.zoom()
                .scaleExtent([0.1, 8])
                .on("zoom", (event) => {
                    g.attr("transform", event.transform);
                });
            
            svg.call(zoom);
            
            // Create arrow markers
            createEnhancedArrowMarkers();
            
            // Create separate containers for each layout
            hierarchicalContainer = g.append("g").attr("class", "hierarchical-layout");
            forceDirectedContainer = g.append("g").attr("class", "force-layout").style("display", "none");
            
            // Expose functions globally for controls
            window.switchToLayout = switchToLayout;
            window.calculateCircleRadius = calculateCircleRadius;
            
            // Set up storage for graph elements
            window.graphElements = {
                hierarchical: {},
                force: {}
            };
            
            // Debug information
            console.log("🎯 Graph visualization initialized successfully");
            console.log("📊 Available functions:", {
                switchToLayout: typeof window.switchToLayout,
                calculateCircleRadius: typeof window.calculateCircleRadius
            });
            console.log("🏗️ Containers created:", {
                hierarchical: !!hierarchicalContainer.node(),
                forceDirected: !!forceDirectedContainer.node()
            });
            
            // CRITICAL: Calculate hierarchical layout positions before creating nodes
            console.log("📐 Calculating hierarchical layout positions...");
            const layout = calculateEnhancedHierarchicalLayout();
            
            // Initialize both layouts
            console.log("🚀 Creating hierarchical layout...");
            initializeHierarchicalLayout();
            console.log("🚀 Creating force-directed layout...");
            initializeForceDirectedLayoutNodes();
            
            // Set up initial layout
            console.log("🏁 Setting initial layout to hierarchical...");
            switchToLayout("hierarchical");
            
            console.log("✅ Graph initialization complete");
        }

        // Enhanced arrow markers creation
        function createEnhancedArrowMarkers() {
            const defs = svg.select("defs").empty() ? svg.append("defs") : svg.select("defs");
            
            // Standard arrow
            defs.append("marker")
                .attr("id", "arrowhead")
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 8)
                .attr("refY", 0)
                .attr("markerWidth", 8)
                .attr("markerHeight", 8)
                .attr("orient", "auto")
                .append("path")
                .attr("d", "M0,-5L10,0L0,5")
                .attr("fill", "#666");
            
            // Highlighted arrow (orange)
            defs.append("marker")
                .attr("id", "arrowhead-highlighted")
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 8)
                .attr("refY", 0)
                .attr("markerWidth", 8)
                .attr("markerHeight", 8)
                .attr("orient", "auto")
                .append("path")
                .attr("d", "M0,-5L10,0L0,5")
                .attr("fill", "#ff6600");
            
            // Path highlighted arrow (blue)
            defs.append("marker")
                .attr("id", "arrowhead-path")
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 8)
                .attr("refY", 0)
                .attr("markerWidth", 8)
                .attr("markerHeight", 8)
                .attr("orient", "auto")
                .append("path")
                .attr("d", "M0,-5L10,0L0,5")
                .attr("fill", "#3b82f6");
            
            // Dimmed arrow
            defs.append("marker")
                .attr("id", "arrowhead-dimmed")
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 8)
                .attr("refY", 0)
                .attr("markerWidth", 8)
                .attr("markerHeight", 8)
                .attr("orient", "auto")
                .append("path")
                .attr("d", "M0,-5L10,0L0,5")
                .attr("fill", "#ccc");
        }

        // Simple layout switching function
        function switchToLayout(layoutName) {
            console.log(`🔄 Switching to ${layoutName} layout`);
            currentLayout = layoutName;
            
            if (layoutName === "hierarchical") {
                hierarchicalContainer.style("display", "block");
                forceDirectedContainer.style("display", "none");
                window.graphElements.node = window.graphElements.hierarchical.node;
                window.graphElements.link = window.graphElements.hierarchical.link;
                
                // Stop any running simulation
                if (simulation) {
                    simulation.stop();
                }
            } else if (layoutName === "force") {
                hierarchicalContainer.style("display", "none");
                forceDirectedContainer.style("display", "block");
                window.graphElements.node = window.graphElements.force.node;
                window.graphElements.link = window.graphElements.force.link;
                
                // Start force simulation
                initializeForceDirectedLayout();
            }
            
            // Ensure performance hotspot visualization is applied after layout switch
            setTimeout(() => {
                applyPerformanceHotspotVisualization();
                updateEnhancedVisibility();
            }, 100);
        }

        // Resize handler
        window.addEventListener("resize", function() {
            updateDimensions();
            
            // Recalculate layout if needed
            if (currentLayout === "hierarchical") {
                // Update hierarchical layout positions
                updatePositions();
            } else if (currentLayout === "force" && simulation) {
                // Update force center
                simulation.force("center", d3.forceCenter(width / 2, height / 2));
                simulation.alpha(0.3).restart();
            }
        });

        // Global click handler
        svg.on("click", function(event) {
            if (event.target === this) {
                resetHighlighting();
            }
        });
    """

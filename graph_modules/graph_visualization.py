"""
Graph Visualization Module
=========================

Core D3.js rendering and visualization utilities.
Handles node/link creation, tooltips, event handling, and common graph operations.
"""


def get_graph_visualization_js() -> str:
    """
    Get JavaScript code for core graph visualization functionality.

    Returns:
        str: JavaScript code for graph rendering and utilities
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
        
        // Initialize hierarchical layout (rectangles)
        function initializeHierarchicalLayout() {
            console.log("📊 Creating hierarchical layout with rectangles...");
            
            // Validate and fix node coordinates
            graphData.nodes.forEach((d, i) => {
                if (!d.x || isNaN(d.x) || !d.y || isNaN(d.y)) {
                    console.warn(`⚠️ Invalid coordinates for node ${d.id}, applying fallback positioning`);
                    // Simple fallback grid layout
                    const cols = Math.ceil(Math.sqrt(graphData.nodes.length));
                    d.x = (i % cols) * 150 + 100;
                    d.y = Math.floor(i / cols) * 100 + 100;
                }
                
                // Ensure dimensions exist with improved width calculation
                if (!d.width || isNaN(d.width)) {
                    // More generous width calculation for better text display
                    const baseWidth = Math.max(140, d.stem.length * 9 + 30);
                    d.width = baseWidth;
                }
                if (!d.height || isNaN(d.height)) {
                    d.height = d.folder !== "root" ? 40 : 30;
                }
            });
            
            // Create links for hierarchical layout
            const hierarchicalLinks = hierarchicalContainer.append("g").attr("class", "links");
            const link = hierarchicalLinks.selectAll("path")
                .data(graphData.edges)
                .enter().append("path")
                .attr("class", d => {
                    let classes = "link";
                    if (d.is_test_related) classes += " test-related";
                    return classes;
                })
                .attr("d", d => createEnhancedCubicBezierPath(d))
                .attr("marker-end", "url(#arrowhead)");
            
            // Create nodes for hierarchical layout
            const hierarchicalNodes = hierarchicalContainer.append("g").attr("class", "nodes");
            const node = hierarchicalNodes.selectAll("g")
                .data(graphData.nodes)
                .enter().append("g")
                .attr("class", "node hierarchical-node")
                .attr("transform", d => `translate(${d.x},${d.y})`)
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));
            
            // Add rectangles
            node.append("rect")
                .attr("class", d => {
                    let classes = "node-rect";
                    if (d.hotspot_score && d.hotspot_score > 0.5) classes += " hotspot";
                    if (d.change_classification === "very_high") classes += " very-active";
                    if (d.is_performance_hotspot) classes += " performance-hotspot";
                    return classes;
                })
                .attr("width", d => d.width)
                .attr("height", d => d.height)
                .attr("x", d => -d.width/2)
                .attr("y", d => -d.height/2)
                .attr("fill", d => d.color);
            
            // Add hierarchical-specific indicators
            addHierarchicalIndicators(node);
            
            // Add labels
            addNodeLabels(node);
            
            // Setup event handlers
            node.on("click", handleEnhancedNodeClick)
                .on("mouseover", handleEnhancedMouseOver)
                .on("mouseout", handleEnhancedMouseOut);
            
            // Store references
            window.graphElements = window.graphElements || {};
            window.graphElements.hierarchical = { node, link };
            
            console.log(`✅ Hierarchical layout created with ${node.size()} rectangles`);
        }
        
        // Initialize force-directed layout (circles)
        function initializeForceDirectedLayoutNodes() {
            console.log("🌐 Creating force-directed layout with circles...");
            
            // Debug: Check initial node state
            console.log("📊 Node coordinate check before force layout:");
            graphData.nodes.forEach((d, i) => {
                const isValid = typeof d.x === 'number' && !isNaN(d.x) && typeof d.y === 'number' && !isNaN(d.y);
                console.log(`Node ${d.id}: x=${d.x}, y=${d.y}, valid=${isValid}`);
            });
            
            // Validate and fix node coordinates for force layout too
            graphData.nodes.forEach((d, i) => {
                if (!d.x || isNaN(d.x) || !d.y || isNaN(d.y)) {
                    console.warn(`⚠️ Invalid coordinates for force node ${d.id}, applying fallback positioning`);
                    // Center-based initial positioning for force layout
                    const angle = (i / graphData.nodes.length) * 2 * Math.PI;
                    const radius = Math.min(width, height) / 4;
                    d.x = width / 2 + radius * Math.cos(angle);
                    d.y = height / 2 + radius * Math.sin(angle);
                    console.log(`📍 Fallback position for ${d.id}: x=${d.x}, y=${d.y}`);
                }
            });
            
            // Create links for force-directed layout
            const forceLinks = forceDirectedContainer.append("g").attr("class", "links");
            const link = forceLinks.selectAll("path")
                .data(graphData.edges)
                .enter().append("path")
                .attr("class", d => {
                    let classes = "link";
                    if (d.is_test_related) classes += " test-related";
                    return classes;
                })
                .attr("d", d => createEnhancedCubicBezierPath(d))
                .attr("marker-end", "url(#arrowhead)");
            
            // Create nodes for force-directed layout
            const forceNodes = forceDirectedContainer.append("g").attr("class", "nodes");
            const node = forceNodes.selectAll("g")
                .data(graphData.nodes)
                .enter().append("g")
                .attr("class", "node force-node")
                .attr("transform", d => `translate(${d.x},${d.y})`)
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));
            
            // Add circles with importance-based sizing
            node.append("circle")
                .attr("class", d => {
                    let classes = "node-circle";
                    if (d.hotspot_score && d.hotspot_score > 0.5) classes += " hotspot";
                    if (d.change_classification === "very_high") classes += " very-active";
                    if (d.is_performance_hotspot) classes += " performance-hotspot";
                    return classes;
                })
                .attr("r", d => calculateCircleRadius(d))
                .attr("fill", d => d.color);
            
            // Add labels
            addNodeLabels(node);
            
            // Add change badges positioned for circles
            addCircleChangeBadges(node);
            
            // Setup event handlers
            node.on("click", handleEnhancedNodeClick)
                .on("mouseover", handleEnhancedMouseOver)
                .on("mouseout", handleEnhancedMouseOut);
            
            // Store references
            window.graphElements.force = { node, link };
            
            console.log(`✅ Force-directed layout created with ${node.size()} circles`);
        }
        
        // Initialize force-directed layout with D3.js simulation
        function initializeForceDirectedLayout() {
            console.log("🚀 Starting D3.js force simulation...");
            
            if (!window.graphElements || !window.graphElements.force) {
                console.warn("⚠️ Force elements not found, initializing nodes first");
                initializeForceDirectedLayoutNodes();
            }
            
            const { node, link } = window.graphElements.force;
            
            // Create D3.js force simulation
            simulation = d3.forceSimulation(graphData.nodes)
                .force("link", d3.forceLink(graphData.links)
                    .id(d => d.id)
                    .distance(100)
                    .strength(0.1))
                .force("charge", d3.forceManyBody()
                    .strength(-300)
                    .distanceMax(400))
                .force("center", d3.forceCenter(width / 2, height / 2))
                .force("collision", d3.forceCollide()
                    .radius(d => calculateCircleRadius(d) + 5)
                    .strength(0.7))
                .alpha(0.3)
                .alphaDecay(0.02)
                .velocityDecay(0.4);
            
            // Update positions on each tick
            simulation.on("tick", () => {
                if (currentLayout === "force") {
                    // Update link positions
                    link.attr("d", d => {
                        const source = graphData.nodes[d.source];
                        const target = graphData.nodes[d.target];
                        if (!source || !target) return "";
                        
                        const dx = target.x - source.x;
                        const dy = target.y - source.y;
                        const distance = Math.sqrt(dx * dx + dy * dy);
                        
                        if (distance === 0) return "";
                        
                        const sourceRadius = calculateCircleRadius(source);
                        const targetRadius = calculateCircleRadius(target);
                        
                        // Calculate edge points
                        const sourceX = source.x + (dx / distance) * sourceRadius;
                        const sourceY = source.y + (dy / distance) * sourceRadius;
                        const targetX = target.x - (dx / distance) * targetRadius;
                        const targetY = target.y - (dy / distance) * targetRadius;
                        
                        return `M${sourceX},${sourceY}L${targetX},${targetY}`;
                    });
                    
                    // Update node positions
                    node.attr("transform", d => `translate(${d.x},${d.y})`);
                }
            });
            
            console.log("✅ Force simulation initialized and running");
        }
        
        // Helper function to calculate circle radius based on importance
        function calculateCircleRadius(d) {
            const baseRadius = 20;
            const importance = d.importance || 0;
            const importanceMultiplier = 1 + (importance * 1.5); // Scale up to 2.5x for max importance
            return Math.round(baseRadius * importanceMultiplier);
        }
        
        // Helper function to add hierarchical-specific indicators
        function addHierarchicalIndicators(nodeSelection) {
            // Add importance indicators
            nodeSelection.filter(d => d.importance > 0.3)
                .append("circle")
                .attr("class", d => {
                    if (d.importance > 0.7) return "importance-indicator high";
                    if (d.importance > 0.5) return "importance-indicator medium";
                    return "importance-indicator low";
                })
                .attr("cx", d => d.width/2 - 8)
                .attr("cy", d => -d.height/2 + 8)
                .attr("r", 6);
            
            // Add hotspot indicators
            nodeSelection.filter(d => d.hotspot_score && d.hotspot_score > 0.4)
                .append("circle")
                .attr("class", "hotspot-indicator")
                .attr("cx", d => -d.width/2 + 8)
                .attr("cy", d => -d.height/2 + 8)
                .attr("r", 4)
                .attr("fill", "#ff3333")
                .attr("stroke", "#ffffff")
                .attr("stroke-width", 1);
            
            // Add change frequency badges for rectangles
            nodeSelection.filter(d => d.change_count && d.change_count > 0)
                .append("text")
                .attr("class", "change-badge")
                .attr("x", d => d.width/2 - 12)
                .attr("y", d => d.height/2 - 4)
                .attr("font-size", "10px")
                .attr("fill", "#666")
                .text(d => d.change_count);
        }
        
        // Helper function to add change badges for circles
        function addCircleChangeBadges(nodeSelection) {
            nodeSelection.filter(d => d.change_count && d.change_count > 0)
                .append("text")
                .attr("class", "change-badge")
                .attr("x", d => {
                    const radius = calculateCircleRadius(d);
                    return radius - 8;
                })
                .attr("y", d => {
                    const radius = calculateCircleRadius(d);
                    return radius - 4;
                })
                .attr("font-size", "10px")
                .attr("fill", "#666")
                .text(d => d.change_count);
        }
        
        // Helper function to add node labels (common to both layouts)
        function addNodeLabels(nodeSelection) {
            // Check if this is for circles (force layout) or rectangles (hierarchical layout)
            const isForceLayout = nodeSelection.select("circle").size() > 0;
            
            if (isForceLayout) {
                // For force layout (circles): center text within the circle
                nodeSelection.append("text")
                    .attr("class", "node-label force-node-label")
                    .text(d => d.stem)  // Show full text without truncation
                    .attr("text-anchor", "middle")
                    .attr("dominant-baseline", "central")
                    .attr("dy", "0")
                    .style("font-size", d => {
                        // Scale font size based on circle radius
                        const radius = calculateCircleRadius(d);
                        return `${Math.max(8, Math.min(12, radius / 3))}px`;
                    })
                    .style("font-weight", "bold")
                    .style("pointer-events", "none");
                
                // Folder labels removed as requested
            } else {
                // For hierarchical layout (rectangles): original positioning
                nodeSelection.append("text")
                    .attr("class", "node-label")
                    .text(d => d.stem)
                    .attr("dy", "-2px");
                
                // Folder labels removed as requested
            }
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
        
        // Enhanced event handlers
        function handleEnhancedNodeClick(event, d) {
            event.stopPropagation();
            highlightEnhancedDirectPath(d);
        }
        
        function handleEnhancedMouseOver(event, d) {
            // Calculate predecessors (incoming) and successors (outgoing)
            const predecessors = graphData.edges.filter(e => e.target_name === d.id).length;
            const successors = graphData.edges.filter(e => e.source_name === d.id).length;
            const predecessorNames = graphData.edges.filter(e => e.target_name === d.id)
                .map(e => {
                    const dep = graphData.nodes.find(n => n.id === e.source_name);
                    return dep ? dep.stem : e.source_name;
                }).join(", ");
            const successorNames = graphData.edges.filter(e => e.source_name === d.id)
                .map(e => {
                    const dep = graphData.nodes.find(n => n.id === e.target_name);
                    return dep ? dep.stem : e.target_name;
                }).join(", ");
            
            const importanceLevel = d.importance > 0.7 ? "High" : 
                                  d.importance > 0.5 ? "Medium" : 
                                  d.importance > 0.3 ? "Low" : "Minimal";
            
            tooltip.style("opacity", 1)
                .attr("aria-hidden", "false")
                .html(`
                    <strong>${d.stem}</strong><br/>
                    <strong>Folder:</strong> ${d.folder}<br/>
                    <strong>Importance:</strong> ${importanceLevel} (${(d.importance * 100).toFixed(1)}%)<br/>
                    <strong>Predecessors:</strong> ${predecessors} ${predecessorNames ? `<span style='color:#888'>[${predecessorNames}]</span>` : ''}<br/>
                    <strong>Successors:</strong> ${successors} ${successorNames ? `<span style='color:#888'>[${successorNames}]</span>` : ''}<br/>
                    <strong>File Size:</strong> ${(d.size / 1024).toFixed(1)}KB<br/>
                    ${d.is_test ? "<strong>Type:</strong> Test File<br/>" : ""}
                `)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 10) + "px");
        }
        
        function handleEnhancedMouseOut() {
            tooltip.style("opacity", 0).attr("aria-hidden", "true");
        }
        
        // Enhanced highlighting with dual-mode support
        function highlightEnhancedDirectPath(clickedNode) {
            selectedNode = clickedNode;
            
            if (showCompletePaths) {
                // Advanced highlighting: direct connections (orange) + complete paths (blue)
                const directConnected = findDirectConnections(clickedNode.id);
                const allReachable = findAllReachableNodes(clickedNode.id);
                const pathConnected = new Set([...allReachable].filter(id => !directConnected.has(id)));
                
                // Reset all elements
                window.graphElements.node.classed("dimmed highlighted path-highlighted", false);
                window.graphElements.node.selectAll(".node-rect, .node-circle").classed("dimmed highlighted path-highlighted", false);
                window.graphElements.link
                    .classed("dimmed highlighted path-highlighted", false)
                    .attr("marker-end", "url(#arrowhead)");
                
                // Apply dual highlighting
                window.graphElements.node
                    .classed("highlighted", d => directConnected.has(d.id))
                    .classed("path-highlighted", d => pathConnected.has(d.id))
                    .classed("dimmed", d => !allReachable.has(d.id));
                
                window.graphElements.node.selectAll(".node-rect, .node-circle")
                    .classed("highlighted", function() {
                        const nodeData = d3.select(this.parentNode).datum();
                        return directConnected.has(nodeData.id);
                    })
                    .classed("path-highlighted", function() {
                        const nodeData = d3.select(this.parentNode).datum();
                        return pathConnected.has(nodeData.id);
                    })
                    .classed("dimmed", function() {
                        const nodeData = d3.select(this.parentNode).datum();
                        return !allReachable.has(nodeData.id);
                    });
                
                // Apply dimming to text elements for better visibility
                window.graphElements.node.selectAll(".node-label")
                    .classed("dimmed", function() {
                        const nodeData = d3.select(this.parentNode).datum();
                        return !allReachable.has(nodeData.id);
                    });
                
                // Highlight edges
                window.graphElements.link
                    .classed("highlighted", d => directConnected.has(d.source_name) && directConnected.has(d.target_name))
                    .classed("path-highlighted", d => pathConnected.has(d.source_name) || pathConnected.has(d.target_name))
                    .classed("dimmed", d => !(allReachable.has(d.source_name) && allReachable.has(d.target_name)))
                    .attr("marker-end", d => {
                        if (directConnected.has(d.source_name) && directConnected.has(d.target_name)) {
                            return "url(#arrowhead-highlighted)";
                        } else if (pathConnected.has(d.source_name) || pathConnected.has(d.target_name)) {
                            return "url(#arrowhead-path)";
                        } else if (!(allReachable.has(d.source_name) && allReachable.has(d.target_name))) {
                            return "url(#arrowhead-dimmed)";
                        } else {
                            return "url(#arrowhead)";
                        }
                    });
                
                highlightedNodes = allReachable;
            } else {
                // Simple highlighting: only direct connections (orange)
                const connected = findDirectConnections(clickedNode.id);
                
                // Reset all elements
                window.graphElements.node.classed("dimmed highlighted path-highlighted", false);
                window.graphElements.node.selectAll(".node-rect, .node-circle").classed("dimmed highlighted path-highlighted", false);
                window.graphElements.link
                    .classed("dimmed highlighted path-highlighted", false)
                    .attr("marker-end", "url(#arrowhead)");
                
                // Apply simple highlighting
                window.graphElements.node
                    .classed("highlighted", d => connected.has(d.id))
                    .classed("dimmed", d => !connected.has(d.id));
                
                window.graphElements.node.selectAll(".node-rect, .node-circle")
                    .classed("highlighted", function() {
                        const nodeData = d3.select(this.parentNode).datum();
                        return connected.has(nodeData.id);
                    })
                    .classed("dimmed", function() {
                        const nodeData = d3.select(this.parentNode).datum();
                        return !connected.has(nodeData.id);
                    });
                
                // Apply dimming to text elements for better visibility
                window.graphElements.node.selectAll(".node-label")
                    .classed("dimmed", function() {
                        const nodeData = d3.select(this.parentNode).datum();
                        return !connected.has(nodeData.id);
                    });
                
                window.graphElements.link
                    .classed("highlighted", d => connected.has(d.source_name) && connected.has(d.target_name))
                    .classed("dimmed", d => !(connected.has(d.source_name) && connected.has(d.target_name)))
                    .attr("marker-end", d => {
                        if (connected.has(d.source_name) && connected.has(d.target_name)) {
                            return "url(#arrowhead-highlighted)";
                        } else if (!(connected.has(d.source_name) && connected.has(d.target_name))) {
                            return "url(#arrowhead-dimmed)";
                        } else {
                            return "url(#arrowhead)";
                        }
                    });
                
                highlightedNodes = connected;
            }
        }
        
        function findDirectConnections(nodeId) {
            const connected = new Set([nodeId]);
            
            // Find direct connections only
            graphData.edges.forEach(edge => {
                if (!shouldShowEdge(edge)) return;
                
                if (edge.source_name === nodeId) {
                    connected.add(edge.target_name);
                }
                if (edge.target_name === nodeId) {
                    connected.add(edge.source_name);
                }
            });
            
            return connected;
        }
        
        function findAllReachableNodes(nodeId) {
            const directLineage = new Set([nodeId]);
            
            // Find all ancestors (nodes this node depends on, recursively)
            const findAncestors = (currentId, visited = new Set()) => {
                if (visited.has(currentId)) return;
                visited.add(currentId);
                
                graphData.edges.forEach(edge => {
                    if (!shouldShowEdge(edge)) return;
                    
                    // Follow dependencies: if current node depends on another, that's an ancestor
                    if (edge.source_name === currentId && !visited.has(edge.target_name)) {
                        directLineage.add(edge.target_name);
                        findAncestors(edge.target_name, visited);
                    }
                });
            };
            
            // Find all descendants (nodes that depend on this node, recursively)
            const findDescendants = (currentId, visited = new Set()) => {
                if (visited.has(currentId)) return;
                visited.add(currentId);
                
                graphData.edges.forEach(edge => {
                    if (!shouldShowEdge(edge)) return;
                    
                    // Follow dependents: if another node depends on current, that's a descendant
                    if (edge.target_name === currentId && !visited.has(edge.source_name)) {
                        directLineage.add(edge.source_name);
                        findDescendants(edge.source_name, visited);
                    }
                });
            };
            
            // Build complete direct lineage
            findAncestors(nodeId);
            findDescendants(nodeId);
            
            return directLineage;
        }
        
        function findEnhancedConnections(nodeId) {
            // Backward compatibility - use direct connections when not in path mode
            return findDirectConnections(nodeId);
        }
        
        function resetHighlighting() {
            selectedNode = null;
            highlightedNodes.clear();
            window.graphElements.node.classed("dimmed highlighted path-highlighted", false);
            window.graphElements.node.selectAll(".node-rect, .node-circle").classed("dimmed highlighted path-highlighted", false);
            window.graphElements.node.selectAll(".node-label").classed("dimmed", false);
            window.graphElements.link
                .classed("dimmed highlighted", false)
                .attr("marker-end", "url(#arrowhead)");
        }
        
        // Enhanced drag functions with layout awareness
        function dragstarted(event, d) {
            if (currentLayout === "force" && simulation) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
            }
            d.fx = d.x;
            d.fy = d.y;
        }
        
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
            d.x = event.x;
            d.y = event.y;
            
            if (currentLayout === "hierarchical") {
                updatePositions();
            }
            // For force layout, the simulation handles position updates
        }
        
        function dragended(event, d) {
            if (currentLayout === "force" && simulation) {
                if (!event.active) simulation.alphaTarget(0);
            }
            d.fx = null;
            d.fy = null;
        }
        
        function updatePositions() {
            const nodeElem = window.graphElements.node;
            const linkElem = window.graphElements.link;
            if (!nodeElem || !linkElem) return;
            
            nodeElem.attr("transform", d => `translate(${d.x},${d.y})`);
            
            if (currentLayout === "hierarchical") {
                linkElem.attr("d", d => createEnhancedCubicBezierPath(d));
            }
        }
        
        // Enhanced visibility logic
        function shouldShowEdge(edge) {
            const sourceNode = graphData.nodes.find(n => n.id === edge.source_name);
            const targetNode = graphData.nodes.find(n => n.id === edge.target_name);
            
            if (!sourceNode || !targetNode) return false;
            if (!shouldShowNode(sourceNode) || !shouldShowNode(targetNode)) return false;
            
            if (!showTestDependencies && edge.is_test_related) {
                return false;
            }
            
            return true;
        }
        
        function shouldShowNode(node) {
            // Check folder visibility
            if (!checkedFolders.has(node.folder)) return false;
            
            // Check advanced range filters
            // Count predecessors (incoming edges)
            const predecessors = graphData.edges.filter(e => e.target_name === node.id).length;
            if (predecessors < predecessorsRangeFilter.min || predecessors > predecessorsRangeFilter.max) return false;
            
            // Count successors (outgoing edges)
            const successors = graphData.edges.filter(e => e.source_name === node.id).length;
            if (successors < successorsRangeFilter.min || successors > successorsRangeFilter.max) return false;
            
            // Check file size (convert bytes to KB)
            const sizeKB = node.size / 1024;
            if (sizeKB < sizeRangeFilter.min || sizeKB > sizeRangeFilter.max) return false;
            
            return true;
        }
        
        // Update visibility based on current filters
        function updateEnhancedVisibility() {
            if (!window.graphElements) return;
            
            // Update node visibility with advanced filtering
            window.graphElements.node
                .style("opacity", d => {
                    if (!shouldShowNode(d)) return 0.1;
                    if (!showTestDependencies && d.is_test) return 0.3;
                    return 1;
                })
                .style("display", d => shouldShowNode(d) ? "block" : "none");
            
            // Update link visibility
            window.graphElements.link
                .classed("hidden", d => !shouldShowEdge(d))
                .style("opacity", d => {
                    if (!shouldShowEdge(d)) return 0;
                    return d.is_test_related && !showTestDependencies ? 0.3 : 0.8;
                });
            
            // Apply performance hotspot visualization
            applyPerformanceHotspotVisualization();
        }
        
        function applyPerformanceHotspotVisualization() {
            if (!window.graphElements || !window.graphElements.node) return;
            
            // Apply performance hotspot styling to nodes
            window.graphElements.node.selectAll(".node-rect, .node-circle")
                .classed("performance-hotspot", d => d.is_performance_hotspot === true);
            
            // Update tooltips to include performance information
            window.graphElements.node
                .select("title")
                .text(d => {
                    let tooltip = `${d.name}\\n`;
                    tooltip += `Folder: ${d.folder}\\n`;
                    tooltip += `Imports: ${d.imports_count}\\n`;
                    tooltip += `Size: ${d.size} KB\\n`;
                    tooltip += `Importance: ${(d.importance * 100).toFixed(1)}%\\n`;
                    
                    // Add performance metrics if available
                    if (d.performance_score !== undefined) {
                        tooltip += `\\n--- Performance Metrics ---\\n`;
                        tooltip += `Performance Score: ${(d.performance_score * 100).toFixed(1)}%\\n`;
                        if (d.is_performance_hotspot) {
                            tooltip += `⚠️ PERFORMANCE HOTSPOT\\n`;
                        }
                        tooltip += `Complexity: ${d.cyclomatic_complexity}\\n`;
                        tooltip += `Lines: ${d.total_lines}\\n`;
                        tooltip += `Functions: ${d.function_count}\\n`;
                        tooltip += `Heavy Operations: ${d.heavy_operations}\\n`;
                        tooltip += `Max Nesting: ${d.max_nesting_depth}\\n`;
                    }
                    
                    return tooltip;
                });
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

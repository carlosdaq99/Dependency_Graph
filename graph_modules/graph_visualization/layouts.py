"""
Graph Visualization Layouts Module
=================================

Layout-specific functions for hierarchical and force-directed graph layouts.
Handles initialization and management of different visualization approaches.
"""


def get_layouts_visualization_js() -> str:
    """
    Get JavaScript code for layout-specific visualization functionality.

    Returns:
        str: JavaScript code for hierarchical and force-directed layouts
    """
    return """
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
    """

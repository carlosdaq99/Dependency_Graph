"""
Graph Visualization Rendering Module
===================================

Visual rendering functions, labels, indicators, visibility management, and styling.
Handles node appearance, performance hotspots, and visual updates.
"""


def get_rendering_visualization_js() -> str:
    """
    Get JavaScript code for rendering and visual management functionality.

    Returns:
        str: JavaScript code for rendering, labels, and visual effects
    """
    return """
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
                
                // Add performance warning icons for force layout (above the circle)
                nodeSelection.filter(d => d.is_hotspot)
                    .append("text")
                    .attr("class", "performance-warning-icon")
                    .text("⚠️")
                    .attr("text-anchor", "middle")
                    .attr("dominant-baseline", "central")
                    .attr("dy", d => -calculateCircleRadius(d) - 15)
                    .style("font-size", "14px")
                    .style("pointer-events", "none");
                
                // Folder labels removed as requested
            } else {
                // For hierarchical layout (rectangles): original positioning
                nodeSelection.append("text")
                    .attr("class", "node-label")
                    .text(d => d.stem)
                    .attr("dy", "-2px");
                
                // Add performance warning icons for hierarchical layout (to the right of text)
                nodeSelection.filter(d => d.is_hotspot)
                    .append("text")
                    .attr("class", "performance-warning-icon")
                    .text("⚠️")
                    .attr("text-anchor", "start")
                    .attr("dominant-baseline", "central")
                    .attr("dx", d => {
                        // Position icon to the right of the text
                        const textLength = d.stem.length * 6; // Rough estimate
                        return textLength + 10;
                    })
                    .attr("dy", "-2px")
                    .style("font-size", "12px")
                    .style("pointer-events", "none");
                
                // Folder labels removed as requested
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
    """

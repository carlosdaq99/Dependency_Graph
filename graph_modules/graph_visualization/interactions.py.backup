"""
Graph Visualization Interactions Module
======================================

Event handling, mouse interactions, drag behavior, and user input management.
Handles clicks, hover effects, dragging, and graph interaction logic.
"""


def get_interactions_visualization_js() -> str:
    """
    Get JavaScript code for interaction and event handling functionality.

    Returns:
        str: JavaScript code for user interactions and event management
    """
    return """
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
                
                // Highlight edges - FIXED: Only highlight edges between highlighted nodes
                window.graphElements.link
                    .classed("highlighted", d => directConnected.has(d.source_name) && directConnected.has(d.target_name))
                    .classed("path-highlighted", d => pathConnected.has(d.source_name) && pathConnected.has(d.target_name))
                    .classed("dimmed", d => !(allReachable.has(d.source_name) && allReachable.has(d.target_name)))
                    .attr("marker-end", d => {
                        if (directConnected.has(d.source_name) && directConnected.has(d.target_name)) {
                            return "url(#arrowhead-highlighted)";
                        } else if (pathConnected.has(d.source_name) && pathConnected.has(d.target_name)) {
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
                .classed("dimmed highlighted path-highlighted", false)
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
    """

"""
HTML Generator Module
====================

HTML template assembly and main generation function.
Combines all modules into the complete visualization HTML.
"""

import json
from pathlib import Path
from typing import Dict, Any

from .graph_styles import get_graph_styles
from .graph_visualization import get_graph_visualization_js
from .hierarchical_layout import get_hierarchical_layout_js
from .force_directed_layout import get_force_directed_layout_js
from .graph_controls import get_graph_controls_js


def get_html_head() -> str:
    """
    Get HTML head section with meta tags and external dependencies.

    Returns:
        str: HTML head section
    """
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Dependency Graph</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>{styles}</style>
</head>"""


def get_html_body(project_maximums: Dict[str, int] = None) -> str:
    """
    Get HTML body structure with controls and graph container.

    Args:
        project_maximums: Dict with max_predecessors, max_successors, max_size_kb

    Returns:
        str: HTML body structure with dynamic filter ranges
    """
    # Use provided maximums or defaults
    if project_maximums is None:
        project_maximums = {
            "max_predecessors": 20,
            "max_successors": 20,
            "max_size_kb": 100,
        }

    max_pred = project_maximums["max_predecessors"]
    max_succ = project_maximums["max_successors"]
    max_size = project_maximums["max_size_kb"]
    return """<body>
    <div class="container">
        <div class="controls">
            <div class="section">
                <h3>📊 Statistics</h3>
                <div id="stats-content" class="stats-grid"></div>
            </div>
            
            <div class="section">
                <h3>🎛️ Layout Control</h3>
                <div class="layout-toggle" id="layout-toggle">
                    <span class="layout-toggle-label">📐 Hierarchical</span>
                    <div class="toggle-switch" id="toggle-switch">
                        <div class="toggle-slider"></div>
                    </div>
                    <span class="layout-toggle-label">🌐 Force-Directed</span>
                </div>
                <div class="layout-mode-indicator" id="layout-indicator">
                    Current: Hierarchical Layout
                </div>
            </div>
            
            <div class="section">
                <h3>📁 Directories</h3>
                <div class="folder-item" id="select-all-toggle" role="checkbox" tabindex="0" style="border-bottom: 1px solid #e9ecef; margin-bottom: 10px; padding-bottom: 8px; font-weight: bold;">
                    <span class="folder-checkbox">☑</span>
                    <span class="folder-label">Select All Directories</span>
                </div>
                <div id="folder-controls"></div>
            </div>
            
            <div class="section">
                <h3>🔍 Advanced Filters</h3>
                <div style="margin-bottom: 15px;">
                    <label for="predecessors-filter" class="filter-label">
                        📥 Predecessors (incoming):
                    </label>
                    <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 5px;">
                        <input type="range" id="predecessors-min-filter" min="0" max="{max_pred}" value="0" style="width: 45%;">
                        <span style="font-size: 12px;">to</span>
                        <input type="range" id="predecessors-max-filter" min="0" max="{max_pred}" value="{max_pred}" style="width: 45%;">
                    </div>
                    <div class="filter-value">
                        <span id="predecessors-filter-value">0 - {max_pred}</span> predecessors
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label for="successors-filter" class="filter-label">
                        📤 Successors (outgoing):
                    </label>
                    <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 5px;">
                        <input type="range" id="successors-min-filter" min="0" max="{max_succ}" value="0" style="width: 45%;">
                        <span style="font-size: 12px;">to</span>
                        <input type="range" id="successors-max-filter" min="0" max="{max_succ}" value="{max_succ}" style="width: 45%;">
                    </div>
                    <div class="filter-value">
                        <span id="successors-filter-value">0 - {max_succ}</span> successors
                    </div>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label for="size-filter" class="filter-label">
                        📄 File Size (KB):
                    </label>
                    <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 5px;">
                        <input type="range" id="size-min-filter" min="0" max="{max_size}" value="0" style="width: 45%;">
                        <span style="font-size: 12px;">to</span>
                        <input type="range" id="size-max-filter" min="0" max="{max_size}" value="{max_size}" style="width: 45%;">
                    </div>
                    <div class="filter-value">
                        <span id="size-filter-value">0 - {max_size}</span> KB
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h3>🧪 Test Controls</h3>
                <div class="folder-item" id="test-toggle" role="checkbox" tabindex="0">
                    <span class="folder-checkbox">☑</span>
                    <span class="folder-label">Show Test Dependencies</span>
                </div>
            </div>
            
            <div class="section">
                <h3>🔗 Highlighting Options</h3>
                <div class="folder-item" id="path-highlighting-toggle" role="checkbox" tabindex="0">
                    <span class="folder-checkbox">☐</span>
                    <span class="folder-label">Show Complete Paths</span>
                </div>
                <div style="font-size: 11px; color: var(--text-muted); margin-top: 8px; padding: 0 12px;">
                    When enabled, highlights all nodes reachable by following a continuous path from the selected node (blue), while direct connections remain orange.
                </div>
            </div>
            
            <div class="section">
                <h3>🔧 Controls</h3>
                <button class="reset-button" onclick="resetAllFilters()">Reset All Filters</button>
            </div>
        </div>
        
        <div class="graph-container">
            <div class="theme-toggle" onclick="toggleTheme()">
                <span class="theme-icon">🌙</span>
                <span class="theme-text">Dark</span>
            </div>
            <svg id="graph"></svg>
            <div id="tooltip" class="tooltip" aria-hidden="true"></div>
        </div>
    </div>

    <script>
        // Enhanced graph data with complete directory inclusion
        const graphData = {graph_data_json};

        {visualization_js}
        {hierarchical_layout_js}
        {force_directed_layout_js}
        {controls_js}
        
        // Initialize on load
        document.addEventListener("DOMContentLoaded", function() {{
            initializeTheme();
            initializeEnhancedVisualization();
            initializeControls();
        }});
    </script>
</body>
</html>"""


def calculate_project_maximums(graph_data: Dict[str, Any]) -> Dict[str, int]:
    """
    Calculate actual project maximums for filter ranges.

    Args:
        graph_data: Complete graph data dictionary

    Returns:
        Dict with max_predecessors, max_successors, max_size_kb
    """
    nodes = graph_data.get("nodes", [])
    edges = graph_data.get("edges", [])

    if not nodes:
        return {"max_predecessors": 20, "max_successors": 20, "max_size_kb": 100}

    # Calculate actual maximums
    max_predecessors = 0
    max_successors = 0
    max_size_kb = 0

    for node in nodes:
        # Count predecessors (incoming edges)
        predecessors = len([edge for edge in edges if edge["target"] == node["index"]])
        max_predecessors = max(max_predecessors, predecessors)

        # Count successors (outgoing edges)
        successors = len([edge for edge in edges if edge["source"] == node["index"]])
        max_successors = max(max_successors, successors)

        # File size in KB
        size_kb = node.get("size_kb", 0)
        max_size_kb = max(max_size_kb, size_kb)

    # Add some padding to maximums for better UX
    return {
        "max_predecessors": max_predecessors + 2,
        "max_successors": max_successors + 2,
        "max_size_kb": max(
            int(max_size_kb) + 10, 50
        ),  # Minimum 50KB for reasonable range
    }


def generate_enhanced_html_visualization(graph_data: Dict[str, Any]) -> str:
    """
    Generate complete HTML visualization by assembling all modules.

    Args:
        graph_data: Complete graph data dictionary from dependency analyzer

    Returns:
        str: Complete HTML document with embedded visualization
    """
    print("🎨 Assembling modular HTML visualization...")

    # Calculate project maximums for dynamic filter ranges
    project_maximums = calculate_project_maximums(graph_data)
    print(f"📊 Calculated filter maximums: {project_maximums}")

    # Get all component pieces
    styles = get_graph_styles()
    visualization_js = get_graph_visualization_js()
    hierarchical_layout_js = get_hierarchical_layout_js()
    force_directed_layout_js = get_force_directed_layout_js()
    controls_js = get_graph_controls_js()

    # Get HTML structure
    html_head = get_html_head()
    html_body = get_html_body(project_maximums)  # Pass maximums to body generation

    # Assemble complete HTML with dynamic values
    complete_html = html_head.format(styles=styles) + html_body.format(
        graph_data_json=json.dumps(graph_data, indent=2),
        visualization_js=visualization_js,
        hierarchical_layout_js=hierarchical_layout_js,
        force_directed_layout_js=force_directed_layout_js,
        controls_js=controls_js,
        max_pred=project_maximums["max_predecessors"],
        max_succ=project_maximums["max_successors"],
        max_size=project_maximums["max_size_kb"],
    )

    print("✅ Modular HTML visualization assembled successfully")
    return complete_html


def main(root_path: str = None):
    """Generate enhanced dependency graph with modular architecture.

    Args:
        root_path: Path to the root directory to analyze. If None, uses default logic.
    """
    from .dependency_analyzer import EnhancedDependencyAnalyzer

    print("🚀 ENHANCED DEPENDENCY GRAPH - MODULAR IMPLEMENTATION")
    print("=" * 60)

    # Determine the root path
    if root_path is None:
        # Use existing logic for backward compatibility
        print("📊 Analyzing with automatic root detection...")
        analyzer = EnhancedDependencyAnalyzer()
        graph_data = analyzer.analyze_project()
    else:
        # Use the provided root path
        print(f"📊 Analyzing project at: {root_path}")
        analyzer = EnhancedDependencyAnalyzer()
        graph_data = analyzer.analyze_project(root_path)

    # Generate enhanced HTML visualization
    print("🎨 Generating modular visualization...")
    html_content = generate_enhanced_html_visualization(graph_data)

    # Save files - determine if we're in dependency_graph folder and adjust path accordingly
    current_dir = Path.cwd()
    if (
        current_dir.name == "dependency_graph"
        or (current_dir / "graph_modules").exists()
    ):
        output_dir = Path(
            "graph_output"
        )  # We're in dependency_graph folder, use relative path
    else:
        output_dir = (
            Path("dependency_graph") / "graph_output"
        )  # We're in root, use dependency_graph subfolder
    output_dir.mkdir(exist_ok=True)

    # Save enhanced graph data
    with open(output_dir / "enhanced_graph_data.json", "w") as f:
        json.dump(graph_data, f, indent=2)

    # Save enhanced HTML
    with open(
        output_dir / "enhanced_dependency_graph.html", "w", encoding="utf-8"
    ) as f:
        f.write(html_content)

    print("✅ MODULAR DEPENDENCY GRAPH COMPLETE!")
    print("=" * 50)
    print("📊 Analysis Results:")
    stats = graph_data["statistics"]
    print(f"   - Total files analyzed: {stats['total_files']}")
    print(f"   - Total dependencies: {stats['total_dependencies']}")
    print(f"   - Cross-folder dependencies: {stats['cross_folder_dependencies']}")
    print(f"   - Test files included: {stats['test_files']}")
    print(f"   - Directories included: {stats['folders']}")

    print("\n🏗️ Modular Architecture:")
    print("   ✅ dependency_analyzer.py - Core analysis logic")
    print("   ✅ graph_styles.py - CSS styling definitions")
    print("   ✅ hierarchical_layout.py - Hierarchical layout algorithms")
    print("   ✅ force_directed_layout.py - Force-directed layout algorithms")
    print("   ✅ graph_visualization.py - Core D3.js rendering")
    print("   ✅ graph_controls.py - UI controls and event handling")
    print("   ✅ html_generator.py - HTML template assembly")

    print("\n🎯 Key Features:")
    print("   ✅ Modular, maintainable codebase")
    print("   ✅ Easy to extend and debug individual components")
    print("   ✅ Clean separation of concerns")
    print("   ✅ Complete directory inclusion (including tests, assets, reports)")
    print("   ✅ Enhanced hierarchical layout with importance-based positioning")
    print("   ✅ Force-directed layout toggle with D3.js simulation")
    print("   ✅ Smooth layout transitions and animations")
    print("   ✅ Advanced filtering and interactive controls")

    print("\n📄 Generated Files:")
    print("   - Enhanced graph data: graph_output/enhanced_graph_data.json")
    print("   - Enhanced visualization: graph_output/enhanced_dependency_graph.html")
    print("\n📁 Modular Components:")
    print("   - graph_modules/ - All modular components")
    print("   - graph_modules/__init__.py - Package initialization")
    print("   - graph_modules/dependency_analyzer.py - Analysis logic")
    print("   - graph_modules/graph_styles.py - CSS styling")
    print("   - graph_modules/hierarchical_layout.py - Hierarchical layouts")
    print("   - graph_modules/force_directed_layout.py - Force layouts")
    print("   - graph_modules/graph_visualization.py - Core visualization")
    print("   - graph_modules/graph_controls.py - UI controls")
    print("   - graph_modules/html_generator.py - HTML generation")

    return graph_data

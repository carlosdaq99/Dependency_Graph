#!/usr/bin/env python3
"""
Enhanced Dependency Graph - Modular Implementation
=================================================

Main entry point for the modularized enhanced dependency graph system.
This replaces the monolithic enhanced_dependency_graph.py with a clean,
maintainable modular architecture.

Usage:
    python enhanced_dependency_graph_modular.py [root_path]

    root_path: Path to the root directory to analyze (optional, defaults to parent directory)
    Examples:
        python enhanced_dependency_graph_modular.py
        python enhanced_dependency_graph_modular.py "C:/path/to/project"
        python enhanced_dependency_graph_modular.py "/home/user/project"

The original enhanced_dependency_graph.py has been split into focused modules:
- dependency_analyzer.py: Core analysis logic
- graph_styles.py: CSS styling
- hierarchical_layout.py: Hierarchical layout algorithms
- force_directed_layout.py: Force-directed layout algorithms
- graph_visualization.py: Core D3.js rendering
- graph_controls.py: UI controls and event handling
- html_generator.py: HTML template assembly

Author: Enhanced Dependency Graph System
Date: 2025-07-22
"""

import sys
from pathlib import Path

# USER CONFIGURABLE ROOT DIRECTORY
# Change this path to analyze a different project:
DEFAULT_ROOT_PATH = (
    r"c:\Users\dea29431.RSKGAD\OneDrive - Rsk Group Limited\Documents\Geotech"
    r"\AGS Section\Geo_Borehole_Sections_Render"
)

# Fall back to current directory context (when run from dependency_graph/)
from graph_modules import main

if __name__ == "__main__":
    # Get root path from command line argument or use default
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
        print(f"📁 Using command-line root path: {root_path}")
    else:
        root_path = DEFAULT_ROOT_PATH
        print(f"📁 Using default root path: {root_path}")

    # Validate root path exists
    if not Path(root_path).exists():
        print(f"❌ Error: Root path does not exist: {root_path}")
        print("💡 Usage: python enhanced_dependency_graph_modular.py [root_path]")
        sys.exit(1)

    # Run main with custom root path
    main(root_path)

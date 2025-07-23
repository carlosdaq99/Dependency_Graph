"""
Graph Visualization Module
=========================

Core D3.js rendering and visualization utilities.
Handles node/link creation, tooltips, event handling, and common graph operations.

This module has been refactored into smaller submodules for better maintainability.
The original API is preserved for backward compatibility.
"""

# Import the main function from the refactored submodule
from .graph_visualization import get_graph_visualization_js

# Re-export for backward compatibility
__all__ = ["get_graph_visualization_js"]

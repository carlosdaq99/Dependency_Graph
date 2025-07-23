"""
Graph Visualization Module
=========================

Core D3.js rendering and visualization utilities split into focused components.

Submodules:
- core: Core initialization, state management, and D3.js setup
- layouts: Layout-specific functions (hierarchical and force-directed)
- interactions: Event handling, mouse interactions, and drag behavior
- rendering: Visual rendering, labels, indicators, and styling

This module maintains the original API by combining all submodules.
"""

from .core import get_core_visualization_js
from .layouts import get_layouts_visualization_js
from .interactions import get_interactions_visualization_js
from .rendering import get_rendering_visualization_js


def get_graph_visualization_js() -> str:
    """
    Get JavaScript code for complete graph visualization functionality.

    This function maintains backward compatibility by combining all submodules
    into a single JavaScript string, exactly as the original module did.

    Returns:
        str: Complete JavaScript code for graph rendering and utilities
    """
    # Combine all JavaScript components in the correct order
    components = [
        get_core_visualization_js(),
        get_layouts_visualization_js(),
        get_interactions_visualization_js(),
        get_rendering_visualization_js(),
    ]

    return "\n".join(components)


# Expose the main function for backward compatibility
__all__ = ["get_graph_visualization_js"]

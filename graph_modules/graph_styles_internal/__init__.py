"""
Graph Styles Module
==================

CSS styling for the dependency graph visualization.
Provides theme support, node styling, controls, and responsive design.

This module is split into:
- base_styles: Core CSS, theme variables, and basic elements
- layout_styles: Component layouts, animations, and responsive design
"""

from .base_styles import get_base_styles_css
from .layout_styles import get_layout_styles_css


def get_styles() -> str:
    """
    Get the complete CSS styles for the dependency graph.
    
    Returns:
        str: Complete CSS code combining base and layout styles
    """
    return f"""
        {get_base_styles_css()}
        
        {get_layout_styles_css()}
    """


# Maintain backward compatibility
def get_css_styles() -> str:
    """
    Legacy function name for backward compatibility.
    
    Returns:
        str: Complete CSS styles for the dependency graph
    """
    return get_styles()


# Export all functions for backward compatibility
__all__ = [
    'get_styles',
    'get_css_styles',
    'get_base_styles_css',
    'get_layout_styles_css'
]

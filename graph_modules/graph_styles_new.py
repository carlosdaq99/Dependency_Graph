"""
Graph Styles Module - Backward Compatibility Layer
==================================================

This module maintains backward compatibility with the original graph_styles.py API
while delegating to the refactored submodule structure.

The actual implementation is now split across:
- graph_styles/base_styles.py: Core CSS, theme variables, and basic elements
- graph_styles/layout_styles.py: Component layouts, animations, and responsive design
"""

# Import from the new submodule structure
from .graph_styles import get_styles as _get_styles
from .graph_styles import get_css_styles as _get_css_styles


def get_styles() -> str:
    """
    Returns CSS styles for the dependency graph visualization.

    This function maintains backward compatibility with the original API
    while delegating to the refactored submodule structure.

    Returns:
        str: Complete CSS styles combining base and layout styles
    """
    return _get_styles()


# Legacy alias for backward compatibility
def get_css_styles() -> str:
    """
    Legacy function name for backward compatibility.

    Returns:
        str: Complete CSS styles for the dependency graph
    """
    return _get_css_styles()

"""
Graph Controls Module
====================

JavaScript UI controls, event handling, and filter management split into focused components.

Submodules:
- ui_controls: UI control generation, layout management, and visual interface components
- event_handlers: Event handling and state management for user interactions

This module maintains the original API by combining both submodules.
"""

from .ui_controls import get_ui_controls_js
from .event_handlers import get_event_handlers_js


def get_graph_controls_js() -> str:
    """
    Get JavaScript code for UI controls and event handling.

    This function maintains backward compatibility by combining both submodules
    into a single JavaScript string, exactly as the original module did.

    Returns:
        str: JavaScript code for controls and interaction
    """
    # Combine both JavaScript components
    components = [get_ui_controls_js(), get_event_handlers_js()]

    return "\n".join(components)


# Expose the main function for backward compatibility
# Export all functions for backward compatibility
__all__ = ["get_graph_controls_js", "get_controls_js"]


# Add legacy alias for maximum compatibility
def get_controls_js() -> str:
    """
    Legacy alias for get_graph_controls_js().

    Returns:
        str: Complete JavaScript code for graph controls
    """
    return get_graph_controls_js()

"""
Graph Controls Module
====================

JavaScript UI controls, event handling, and filter management.
Handles layout switching, folder toggles, advanced filters, and statistics.

This module has been refactored into smaller submodules for better maintainability.
The original API is preserved for backward compatibility.
"""

# Import the main function from the refactored submodule
from .graph_controls import get_graph_controls_js

# Re-export for backward compatibility
__all__ = ["get_graph_controls_js"]

"""
Enhanced Dependency Analyzer Module
===================================

Sophisticated dependency analysis functionality split into focused components.

Submodules:
- core: Main EnhancedDependencyAnalyzer class and orchestration
- import_resolver: Import detection, resolution, and mapping
- metrics: Performance analysis, complexity metrics, and importance calculations

This module maintains the original API by exposing the main class.
"""

from .core import EnhancedDependencyAnalyzer

# Re-export for backward compatibility
__all__ = ["EnhancedDependencyAnalyzer"]

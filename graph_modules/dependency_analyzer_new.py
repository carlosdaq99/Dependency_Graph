"""
Enhanced Dependency Analyzer for Comprehensive Code Architecture Analysis.

This module provides sophisticated dependency analysis functionality for Python projects,
offering deep insights into module relationships, import patterns, and architectural
structure. It's specifically designed to analyze complex applications like the Geo
Borehole Sections Render project and generate comprehensive dependency visualizations.

Key Features:
- **Complete Project Scanning**: Analyzes all Python files including test directories
- **Import Relationship Mapping**: Tracks both internal and external dependencies
- **Importance Scoring**: PageRank-style algorithm to identify critical modules
- **Circular Dependency Detection**: Identifies and reports dependency cycles
- **Graph Data Generation**: Creates structured data for visualization tools

Analysis Capabilities:
1. **Module Dependency Mapping**: Tracks which modules import which other modules
2. **Internal vs External Dependencies**: Distinguishes project modules from external libraries
3. **Import Frequency Analysis**: Identifies most commonly imported modules
4. **Dependency Depth Analysis**: Calculates how deep dependency chains go
5. **Critical Path Identification**: Finds modules that many others depend on

Enhanced Features:
- **AST-Based Parsing**: Uses Abstract Syntax Trees for accurate import detection
- **Directory Inclusion**: Includes all directories including tests and utilities
- **Importance Calculation**: Weighted scoring based on dependency relationships
- **Graph Data Structure**: Optimized data format for interactive visualizations
- **Extensible Architecture**: Easy to add new analysis metrics and capabilities

Data Output:
- Nodes: Module information with importance scores and metadata
- Edges: Dependency relationships with strength indicators
- Statistics: Overall project metrics and dependency patterns
- Clusters: Groups of related modules for better visualization

Dependencies:
- ast: Python Abstract Syntax Tree parsing for accurate import analysis
- pathlib: Modern path handling for cross-platform compatibility

This module has been refactored into smaller submodules for better maintainability.
The original API is preserved for backward compatibility.

Author: [Project Team]
Last Modified: July 2025
"""

# Import the main class from the refactored submodule
from .dependency_analyzer import EnhancedDependencyAnalyzer

# Re-export for backward compatibility
__all__ = ["EnhancedDependencyAnalyzer"]

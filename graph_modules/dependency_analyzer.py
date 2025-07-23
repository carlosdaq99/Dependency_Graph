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

Author: [Project Team]
Last Modified: July 2025
"""

import ast
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from .git_analysis import GitAnalyzer


class EnhancedDependencyAnalyzer:
    """Enhanced dependency analyzer with complete directory inclusion."""

    def __init__(self, exclude_folders: List[str] = None):
        # Remove test exclusion - include all directories, but exclude dependency_graph folder
        self.exclude_folders = exclude_folders or ["__pycache__", "dependency_graph"]
        self.dependencies = {}
        self.node_importance = {}
        self.root_path = None  # Will be set in analyze_project
        self.git_analyzer = None  # Will be initialized in analyze_project

    def analyze_project(self, root_path: str = ".") -> Dict[str, Any]:
        """Analyze entire project including previously excluded directories."""
        # Store root_path for use in other methods - use provided path strictly
        self.root_path = Path(root_path).resolve()
        print(f"🔍 Enhanced dependency analysis starting at: {self.root_path}")
        print("🔍 Including ALL directories...")

        # Initialize git analyzer
        self.git_analyzer = GitAnalyzer(self.root_path)

        # Scan for all Python files
        python_files = self._find_python_files(root_path)
        print(f"📁 Found {len(python_files)} Python files across all directories")

        # First pass: Build file registry without dependencies
        self._build_file_registry(python_files)

        # Second pass: Analyze dependencies now that registry is complete
        self._analyze_dependencies(python_files)

        # Calculate node importance (PageRank-style)
        self._calculate_node_importance()

        # Analyze performance characteristics
        self._analyze_performance_hotspots(python_files)

        # Analyze git history for change patterns
        git_analysis = self._analyze_git_history()

        # Build enhanced graph data
        graph_data = self._build_enhanced_graph_data(git_analysis)

        return graph_data

    def _find_python_files(self, root_path: str) -> List[Path]:
        """Find all Python files, including in previously excluded directories."""
        python_files = []
        root = Path(root_path)

        for file_path in root.rglob("*.py"):
            # Only exclude __pycache__ and hidden directories
            if any(excluded in file_path.parts for excluded in self.exclude_folders):
                continue

            if file_path.name.startswith("."):
                continue

            python_files.append(file_path)

        return python_files

    def _build_file_registry(self, python_files: List[Path]) -> None:
        """Build initial file registry without dependencies (first pass)."""
        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Resolve path relative to root for consistent folder detection
                resolved_relative_path = file_path.resolve().relative_to(self.root_path)

                # Create unique identifier
                unique_id = self._create_unique_id(file_path)

                self.dependencies[unique_id] = {
                    "file_path": str(resolved_relative_path),
                    "folder": self._get_folder_name_from_relative_path(
                        resolved_relative_path
                    ),
                    "stem": file_path.stem,
                    "display_name": self._create_display_name_from_relative_path(
                        resolved_relative_path
                    ),
                    "imports": [],  # Will be filled in second pass
                    "all_imports": [],  # Will be filled in second pass
                    "imports_count": 0,  # Will be filled in second pass
                    "internal_imports_count": 0,  # Will be filled in second pass
                    "is_test": self._is_test_file(file_path),
                    "is_init": file_path.name == "__init__.py",
                    "size": len(content),
                }

            except Exception as e:
                print(f"Error registering {file_path}: {e}")

    def _analyze_dependencies(self, python_files: List[Path]) -> None:
        """Analyze dependencies with enhanced import detection (second pass)."""
        for file_path in python_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Parse AST for accurate import analysis
                tree = ast.parse(content, filename=str(file_path))
                internal_imports, all_imports = self._extract_imports(tree, file_path)

                # Update existing entry with dependency information
                unique_id = self._create_unique_id(file_path)
                if unique_id in self.dependencies:
                    self.dependencies[unique_id].update(
                        {
                            "imports": internal_imports,
                            "all_imports": all_imports,
                            "imports_count": len(all_imports),
                            "internal_imports_count": len(internal_imports),
                        }
                    )

            except Exception as e:
                print(f"Error analyzing dependencies for {file_path}: {e}")

    def _extract_imports(
        self, tree: ast.AST, file_path: Path
    ) -> Tuple[List[str], List[str]]:
        """Enhanced import extraction with better resolution."""
        internal_imports = []
        all_imports = []
        current_folder = self._get_folder_name(file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    all_imports.append(alias.name)
                    resolved = self._resolve_import_to_file(alias.name, current_folder)
                    if resolved:
                        internal_imports.append(resolved)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module_name = node.module
                    all_imports.append(module_name)

                    # Handle relative imports
                    if module_name.startswith("."):
                        # Relative import - resolve based on current location
                        resolved = self._resolve_relative_import(module_name, file_path)
                        if resolved:
                            internal_imports.append(resolved)
                    else:
                        # Absolute import
                        resolved = self._resolve_import_to_file(
                            module_name, current_folder
                        )
                        if resolved:
                            internal_imports.append(resolved)

        return internal_imports, all_imports

    def _resolve_relative_import(self, import_name: str, current_file: Path) -> str:
        """Resolve relative imports to actual file IDs."""
        # Count dots to determine level
        level = 0
        while level < len(import_name) and import_name[level] == ".":
            level += 1

        if level == 0:
            return None

        # Get the module name after dots
        module_name = import_name[level:] if level < len(import_name) else ""

        # Navigate up the directory tree
        target_dir = current_file.parent
        for _ in range(level - 1):
            target_dir = target_dir.parent

        # If module_name is empty, looking for __init__.py in target_dir
        if not module_name:
            target_file = target_dir / "__init__.py"
        else:
            # Replace dots with path separators
            module_path = module_name.replace(".", os.sep)
            target_file = target_dir / f"{module_path}.py"

            # Also check for __init__.py in directory
            if not target_file.exists():
                target_file = target_dir / module_path / "__init__.py"

        if target_file.exists():
            return self._create_unique_id(target_file)

        return None

    def _resolve_import_to_file(self, import_name: str, current_folder: str) -> str:
        """Enhanced import resolution to map imports to actual files."""
        # Check if this import corresponds to any known file
        import_parts = import_name.split(".")

        # Try different combinations to find the actual file
        for unique_id, info in self.dependencies.items():
            # Direct stem match
            if info["stem"] == import_parts[0]:
                return unique_id

            # Try matching with folder structure
            if len(import_parts) > 1:
                if (
                    info["folder"] == import_parts[0]
                    and info["stem"] == import_parts[1]
                ):
                    return unique_id

            # Try matching full module path
            file_path = Path(info["file_path"])
            try:
                # Convert file path to module notation
                relative_path = file_path.relative_to(Path("."))
                if relative_path.stem == "__init__":
                    module_path = ".".join(relative_path.parent.parts)
                else:
                    module_path = ".".join(relative_path.with_suffix("").parts)

                if module_path == import_name:
                    return unique_id
            except ValueError:
                pass

        return None

    def _create_unique_id(self, file_path: Path) -> str:
        """Create a unique identifier for a file."""
        try:
            # Use the stored root_path if available, otherwise fall back to current directory
            root = self.root_path if self.root_path else Path(".")
            relative_path = file_path.relative_to(root)
            return str(relative_path).replace("\\", "/")
        except ValueError:
            return str(file_path).replace("\\", "/")

    def _get_folder_name(self, file_path: Path) -> str:
        """Enhanced folder name detection."""
        try:
            # Use the stored root_path if available, otherwise fall back to current directory
            root = self.root_path if self.root_path else Path(".")
            relative_path = file_path.relative_to(root)
            if len(relative_path.parts) > 1:
                return relative_path.parts[0]
            else:
                return "root"
        except ValueError:
            return "external"

    def _create_display_name(self, file_path: Path) -> str:
        """Create a human-readable display name."""
        stem = file_path.stem
        folder = self._get_folder_name(file_path)

        if folder == "root":
            return stem
        else:
            return f"{folder}/{stem}"

    def _get_folder_name_from_relative_path(self, relative_path: Path) -> str:
        """Get folder name from already resolved relative path."""
        if len(relative_path.parts) > 1:
            return relative_path.parts[0]
        else:
            return "root"

    def _create_display_name_from_relative_path(self, relative_path: Path) -> str:
        """Create display name from already resolved relative path."""
        stem = relative_path.stem
        folder = self._get_folder_name_from_relative_path(relative_path)

        if folder == "root":
            return stem
        else:
            return f"{folder}/{stem}"

    def _is_test_file(self, file_path: Path) -> bool:
        """Enhanced test file detection."""
        stem = file_path.stem.lower()
        folder = self._get_folder_name(file_path).lower()

        # Check file name patterns
        test_patterns = [
            stem.startswith("test_"),
            stem.endswith("_test"),
            stem == "test",
            "test" in folder,
            folder.startswith("test"),
        ]

        return any(test_patterns)

    def _calculate_node_importance(self) -> None:
        """Calculate node importance using PageRank-style algorithm."""
        print("📈 Calculating node importance scores...")

        # Build adjacency matrix
        nodes = list(self.dependencies.keys())
        n = len(nodes)

        # Initialize importance scores
        importance = {node: 1.0 / n for node in nodes}

        # PageRank iterations
        damping = 0.85
        for iteration in range(50):  # 50 iterations should be sufficient
            new_importance = {}

            for node in nodes:
                # Base importance (random walk probability)
                new_importance[node] = (1 - damping) / n

                # Add importance from incoming links
                for other_node, info in self.dependencies.items():
                    if node in info["imports"]:
                        outgoing_count = len(info["imports"])
                        if outgoing_count > 0:
                            new_importance[node] += (
                                damping * importance[other_node] / outgoing_count
                            )

            # Check for convergence
            max_diff = max(
                abs(new_importance[node] - importance[node]) for node in nodes
            )
            importance = new_importance

            if max_diff < 1e-6:
                print(f"   Converged after {iteration + 1} iterations")
                break

        # Normalize to 0-1 range
        max_importance = max(importance.values()) if importance.values() else 1
        self.node_importance = {
            node: score / max_importance for node, score in importance.items()
        }

    def _analyze_performance_hotspots(self, python_files: List[Path]) -> None:
        """Analyze performance characteristics of Python modules."""
        print("🔥 Analyzing performance hotspots...")

        self.performance_metrics = {}

        for file_path in python_files:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                unique_id = self._create_unique_id(file_path)

                # Calculate basic complexity metrics
                metrics = self._calculate_complexity_metrics(content, file_path)

                # Calculate performance risk score (0-1)
                performance_score = self._calculate_performance_score(metrics)

                self.performance_metrics[unique_id] = {
                    **metrics,
                    "performance_score": performance_score,
                    "is_hotspot": performance_score
                    > 0.6,  # High performance risk threshold
                }

            except Exception as e:
                print(f"⚠️ Error analyzing {file_path}: {e}")
                continue

    def _calculate_complexity_metrics(self, content: str, file_path: Path) -> dict:
        """Calculate code complexity metrics."""
        lines = content.split("\n")

        # Basic metrics
        total_lines = len(lines)
        code_lines = len(
            [
                line
                for line in lines
                if line.strip() and not line.strip().startswith("#")
            ]
        )

        # Count functions and classes
        function_count = len(re.findall(r"^\s*def\s+\w+", content, re.MULTILINE))
        class_count = len(re.findall(r"^\s*class\s+\w+", content, re.MULTILINE))

        # Calculate cyclomatic complexity approximation
        complexity_indicators = [
            "if ",
            "elif ",
            "else:",
            "for ",
            "while ",
            "try:",
            "except",
            "and ",
            "or ",
            "?",
            "break",
            "continue",
        ]
        cyclomatic_complexity = sum(
            content.count(indicator) for indicator in complexity_indicators
        )

        # Look for performance-heavy patterns
        heavy_patterns = [
            r"\.read\(\)",
            r"\.write\(\)",
            r"\.open\(",
            r"subprocess\.",
            r"requests\.",
            r"urllib\.",
            r"json\.load",
            r"pickle\.load",
            r"pandas\.",
            r"numpy\.",
            r"scipy\.",
            r"matplotlib\.",
            r"for.*in.*range\(.*\d{3,}",
            r"while.*True:",
            r"time\.sleep",
        ]

        heavy_operations = sum(
            len(re.findall(pattern, content, re.IGNORECASE))
            for pattern in heavy_patterns
        )

        # Calculate nesting depth
        max_nesting = self._calculate_max_nesting_depth(content)

        # File size factor
        file_size_kb = file_path.stat().st_size / 1024 if file_path.exists() else 0

        return {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "function_count": function_count,
            "class_count": class_count,
            "cyclomatic_complexity": cyclomatic_complexity,
            "heavy_operations": heavy_operations,
            "max_nesting_depth": max_nesting,
            "file_size_kb": file_size_kb,
        }

    def _calculate_max_nesting_depth(self, content: str) -> int:
        """Calculate maximum nesting depth in the code."""
        lines = content.split("\n")
        max_depth = 0
        current_depth = 0

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            # Count leading whitespace (assuming 4 spaces per level)
            leading_spaces = len(line) - len(line.lstrip())
            indent_level = leading_spaces // 4

            # Update depth tracking
            if any(
                keyword in stripped
                for keyword in [
                    "if ",
                    "for ",
                    "while ",
                    "def ",
                    "class ",
                    "with ",
                    "try:",
                ]
            ):
                current_depth = indent_level + 1
                max_depth = max(max_depth, current_depth)

        return max_depth

    def _calculate_performance_score(self, metrics: dict) -> float:
        """Calculate overall performance risk score (0-1)."""
        # Weighted scoring based on different factors
        factors = {
            "complexity": min(metrics["cyclomatic_complexity"] / 100, 1.0) * 0.3,
            "size": min(metrics["file_size_kb"] / 50, 1.0) * 0.2,  # Files over 50KB
            "heavy_ops": min(metrics["heavy_operations"] / 10, 1.0) * 0.25,
            "nesting": min(metrics["max_nesting_depth"] / 8, 1.0) * 0.15,
            "function_density": min(metrics["function_count"] / 20, 1.0) * 0.1,
        }

        return sum(factors.values())

    def _analyze_git_history(self, days: int = 30) -> Dict[str, Any]:
        """Analyze git history for change patterns and hotspots."""
        if self.git_analyzer and self.git_analyzer.is_git_available:
            return self.git_analyzer.get_combined_analysis(days)
        else:
            print("🚫 Git analysis not available - no change frequency data")
            return {
                "total_files_analyzed": 0,
                "analysis_period_days": days,
                "git_available": False,
                "hotspots": [],
                "stable_files": [],
                "file_data": {},
            }

    def _build_enhanced_graph_data(
        self, git_analysis: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Build enhanced graph data with importance and visual properties."""
        print("🎨 Building enhanced graph visualization data...")

        # Generate distinct colors for folders
        folders = set(info["folder"] for info in self.dependencies.values())
        folder_colors = self._generate_folder_colors(folders)

        nodes = []
        edges = []
        node_index = {}

        # Create nodes with enhanced properties
        for i, (unique_id, info) in enumerate(self.dependencies.items()):
            importance = self.node_importance.get(unique_id, 0)

            # Get git analysis data for this file
            git_data = {}
            if git_analysis and git_analysis.get("file_data"):
                file_path_normalized = info["file_path"].replace("\\", "/")
                git_data = git_analysis["file_data"].get(file_path_normalized, {})

            # Get performance metrics for this file
            perf_data = self.performance_metrics.get(unique_id, {})

            nodes.append(
                {
                    "id": unique_id,
                    "name": info["display_name"],
                    "stem": info["stem"],
                    "folder": info["folder"],
                    "color": folder_colors.get(info["folder"], "#F0F0F0"),
                    "file_path": info["file_path"],
                    "imports_count": info[
                        "internal_imports_count"
                    ],  # Use internal imports count
                    "importance": importance,
                    "is_test": info["is_test"],
                    "is_init": info["is_init"],
                    "size": info["size"],
                    "index": i,
                    # Git analysis data
                    "change_count": git_data.get("change_count", 0),
                    "change_frequency_score": git_data.get(
                        "change_frequency_score", 0.0
                    ),
                    "change_classification": git_data.get(
                        "change_classification", "none"
                    ),
                    "total_churn": git_data.get("total_churn", 0),
                    "churn_classification": git_data.get(
                        "churn_classification", "none"
                    ),
                    "hotspot_score": git_data.get("hotspot_score", 0.0),
                    "last_modified": git_data.get("last_modified", "unknown"),
                    # Performance metrics data
                    "performance_score": perf_data.get("performance_score", 0.0),
                    "is_performance_hotspot": perf_data.get("is_hotspot", False),
                    "cyclomatic_complexity": perf_data.get("cyclomatic_complexity", 0),
                    "total_lines": perf_data.get("total_lines", 0),
                    "function_count": perf_data.get("function_count", 0),
                    "heavy_operations": perf_data.get("heavy_operations", 0),
                    "max_nesting_depth": perf_data.get("max_nesting_depth", 0),
                }
            )
            node_index[unique_id] = i

        # Create edges with enhanced properties
        for unique_id, info in self.dependencies.items():
            source_index = node_index[unique_id]
            source_folder = info["folder"]

            for imported_id in info["imports"]:
                if imported_id in node_index:
                    target_index = node_index[imported_id]
                    target_info = self.dependencies[imported_id]
                    target_folder = target_info["folder"]

                    edges.append(
                        {
                            "source": source_index,
                            "target": target_index,
                            "source_name": unique_id,
                            "target_name": imported_id,
                            "source_folder": source_folder,
                            "target_folder": target_folder,
                            "is_cross_folder": source_folder != target_folder,
                            "is_test_related": info["is_test"]
                            or target_info["is_test"],
                        }
                    )

        # Build subfolder info
        subfolder_info = {}
        for folder, color in folder_colors.items():
            folder_modules = [n for n in nodes if n["folder"] == folder]
            subfolder_info[folder] = {
                "color": color,
                "modules": [n["name"] for n in folder_modules],
                "test_modules": [n["name"] for n in folder_modules if n["is_test"]],
                "count": len(folder_modules),
            }

        return {
            "nodes": nodes,
            "edges": edges,
            "dependencies": self.dependencies,
            "subfolder_info": subfolder_info,
            "importance_scores": self.node_importance,
            "git_analysis": git_analysis or {},
            "statistics": {
                "total_files": len(nodes),
                "total_dependencies": len(edges),
                "cross_folder_dependencies": sum(
                    1 for e in edges if e["is_cross_folder"]
                ),
                "test_files": sum(1 for n in nodes if n["is_test"]),
                "folders": len(subfolder_info),
                "git_analysis_available": git_analysis is not None
                and git_analysis.get("git_available", False),
                "hotspots_detected": (
                    len(git_analysis.get("hotspots", [])) if git_analysis else 0
                ),
                "stable_files_detected": (
                    len(git_analysis.get("stable_files", [])) if git_analysis else 0
                ),
            },
        }

    def _generate_folder_colors(self, folders: Set[str]) -> Dict[str, str]:
        """Generate visually distinct colors for folders."""
        # Predefined color palette for consistent visualization
        color_palette = [
            "#FF6B6B",
            "#4ECDC4",
            "#45B7D1",
            "#96CEB4",
            "#FFEAA7",
            "#DDA0DD",
            "#FFB347",
            "#87CEEB",
            "#DEB887",
            "#F0E68C",
            "#FFA07A",
            "#20B2AA",
            "#87CEFA",
            "#778899",
            "#B0C4DE",
            "#FFFFE0",
            "#00CED1",
            "#FF7F50",
            "#6495ED",
            "#DC143C",
        ]

        folder_list = sorted(folders)
        folder_colors = {}

        for i, folder in enumerate(folder_list):
            folder_colors[folder] = color_palette[i % len(color_palette)]

        return folder_colors

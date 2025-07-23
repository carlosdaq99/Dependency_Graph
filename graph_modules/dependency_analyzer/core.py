"""
Enhanced Dependency Analyzer Core Module
========================================

Main EnhancedDependencyAnalyzer class and core analysis functionality.
Handles project scanning, file registry building, and orchestrating the analysis process.
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any

from ..git_analysis import GitAnalyzer
from .import_resolver import ImportResolver
from .metrics import PerformanceAnalyzer, ImportanceCalculator


class EnhancedDependencyAnalyzer:
    """Enhanced dependency analyzer with complete directory inclusion."""

    def __init__(self, exclude_folders: List[str] = None):
        # Remove test exclusion - include all directories, but exclude dependency_graph folder
        self.exclude_folders = exclude_folders or ["__pycache__", "dependency_graph"]
        self.dependencies = {}
        self.node_importance = {}
        self.root_path = None  # Will be set in analyze_project
        self.git_analyzer = None  # Will be initialized in analyze_project

        # Initialize helper components
        self.import_resolver = ImportResolver(self)
        self.performance_analyzer = PerformanceAnalyzer(self)
        self.importance_calculator = ImportanceCalculator(self)

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
        self.importance_calculator.calculate_node_importance()

        # Analyze performance characteristics
        self.performance_analyzer.analyze_performance_hotspots(python_files)

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
                unique_id = self.create_unique_id(file_path)

                self.dependencies[unique_id] = {
                    "file_path": str(resolved_relative_path),
                    "folder": self.get_folder_name_from_relative_path(
                        resolved_relative_path
                    ),
                    "stem": file_path.stem,
                    "display_name": self.create_display_name_from_relative_path(
                        resolved_relative_path
                    ),
                    "imports": [],  # Will be filled in second pass
                    "all_imports": [],  # Will be filled in second pass
                    "imports_count": 0,  # Will be filled in second pass
                    "internal_imports_count": 0,  # Will be filled in second pass
                    "is_test": self.is_test_file(file_path),
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
                internal_imports, all_imports = self.import_resolver.extract_imports(
                    tree, file_path
                )

                # Update existing entry with dependency information
                unique_id = self.create_unique_id(file_path)
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

    def create_unique_id(self, file_path: Path) -> str:
        """Create a unique identifier for a file."""
        try:
            # Use the stored root_path if available, otherwise fall back to current directory
            root = self.root_path if self.root_path else Path(".")
            relative_path = file_path.relative_to(root)
            return str(relative_path).replace("\\", "/")
        except ValueError:
            return str(file_path).replace("\\", "/")

    def get_folder_name(self, file_path: Path) -> str:
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

    def create_display_name(self, file_path: Path) -> str:
        """Create a human-readable display name."""
        stem = file_path.stem
        folder = self.get_folder_name(file_path)

        if folder == "root":
            return stem
        else:
            return f"{folder}/{stem}"

    def get_folder_name_from_relative_path(self, relative_path: Path) -> str:
        """Get folder name from already resolved relative path."""
        if len(relative_path.parts) > 1:
            return relative_path.parts[0]
        else:
            return "root"

    def create_display_name_from_relative_path(self, relative_path: Path) -> str:
        """Create display name from already resolved relative path."""
        stem = relative_path.stem
        folder = self.get_folder_name_from_relative_path(relative_path)

        if folder == "root":
            return stem
        else:
            return f"{folder}/{stem}"

    def is_test_file(self, file_path: Path) -> bool:
        """Enhanced test file detection."""
        stem = file_path.stem.lower()
        folder = self.get_folder_name(file_path).lower()

        # Check file name patterns
        test_patterns = [
            stem.startswith("test_"),
            stem.endswith("_test"),
            stem == "test",
            "test" in folder,
            folder.startswith("test"),
        ]

        return any(test_patterns)

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
            perf_data = self.performance_analyzer.performance_metrics.get(unique_id, {})

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

"""
Metrics Analysis Module
======================

Handles performance analysis, complexity metrics, and importance calculations.
Contains algorithms for calculating node importance and performance hotspots.
"""

import re
from pathlib import Path
from typing import Dict, List


class ImportanceCalculator:
    """Calculates node importance using PageRank-style algorithm."""

    def __init__(self, analyzer):
        """Initialize with reference to the main analyzer."""
        self.analyzer = analyzer

    def calculate_node_importance(self) -> None:
        """Calculate node importance using PageRank-style algorithm."""
        print("📈 Calculating node importance scores...")

        # Build adjacency matrix
        nodes = list(self.analyzer.dependencies.keys())
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
                for other_node, info in self.analyzer.dependencies.items():
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
        self.analyzer.node_importance = {
            node: score / max_importance for node, score in importance.items()
        }


class PerformanceAnalyzer:
    """Analyzes performance characteristics and complexity metrics."""

    def __init__(self, analyzer):
        """Initialize with reference to the main analyzer."""
        self.analyzer = analyzer
        self.performance_metrics = {}

    def analyze_performance_hotspots(self, python_files: List[Path]) -> None:
        """Analyze performance characteristics of Python modules."""
        print("🔥 Analyzing performance hotspots...")

        self.performance_metrics = {}

        for file_path in python_files:
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                unique_id = self.analyzer.create_unique_id(file_path)

                # Calculate basic complexity metrics
                metrics = self.calculate_complexity_metrics(content, file_path)

                # Calculate performance risk score (0-1)
                performance_score = self.calculate_performance_score(metrics)

                self.performance_metrics[unique_id] = {
                    **metrics,
                    "performance_score": performance_score,
                    "is_hotspot": performance_score
                    > 0.6,  # High performance risk threshold
                }

            except Exception as e:
                print(f"⚠️ Error analyzing {file_path}: {e}")
                continue

    def calculate_complexity_metrics(self, content: str, file_path: Path) -> dict:
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
        max_nesting = self.calculate_max_nesting_depth(content)

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

    def calculate_max_nesting_depth(self, content: str) -> int:
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

    def calculate_performance_score(self, metrics: dict) -> float:
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

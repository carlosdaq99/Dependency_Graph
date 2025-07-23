#!/usr/bin/env python3
"""
Test script to validate all imports and basic functionality including performance analysis.
"""

import sys
import traceback
from pathlib import Path


def test_imports():
    """Test all module imports."""
    print("🔍 Testing module imports...")

    try:
        # Test core modules
        from graph_modules.dependency_analyzer import EnhancedDependencyAnalyzer
        from graph_modules import graph_visualization
        from graph_modules import html_generator
        from graph_modules import graph_styles
        from graph_modules import graph_controls

        print("✅ All core module imports successful")

        # Test re module specifically in dependency_analyzer
        import re

        print("✅ re module import successful")

        return True

    except Exception as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False


def test_performance_analysis():
    """Test performance analysis functionality."""
    print("\n🚀 Testing performance analysis...")

    try:
        from graph_modules.dependency_analyzer import EnhancedDependencyAnalyzer

        # Create analyzer instance
        analyzer = EnhancedDependencyAnalyzer()

        # Test if performance analysis methods exist
        assert hasattr(
            analyzer, "_analyze_performance_hotspots"
        ), "Missing _analyze_performance_hotspots method"
        assert hasattr(
            analyzer, "_calculate_complexity_metrics"
        ), "Missing _calculate_complexity_metrics method"
        assert hasattr(
            analyzer, "_calculate_performance_score"
        ), "Missing _calculate_performance_score method"

        print("✅ Performance analysis methods exist")

        # Test complexity calculation with a sample file
        test_file = Path(__file__)
        if test_file.exists():
            with open(test_file, "r", encoding="utf-8") as f:
                content = f.read()

            metrics = analyzer._calculate_complexity_metrics(content, test_file)
            print(f"✅ Complexity metrics calculated: {metrics}")

            score = analyzer._calculate_performance_score(metrics)
            print(f"✅ Performance score calculated: {score}")

        return True

    except Exception as e:
        print(f"❌ Performance analysis error: {e}")
        traceback.print_exc()
        return False


def test_path_highlighting_logic():
    """Test that path highlighting logic is implemented."""
    print("\n🎯 Testing path highlighting logic...")

    try:
        from graph_modules import graph_visualization

        # Check if the JavaScript contains the corrected path highlighting logic
        js_content = graph_visualization.get_graph_visualization_js()

        # Check for direct lineage functions
        assert "findAncestors" in js_content, "Missing findAncestors function"
        assert "findDescendants" in js_content, "Missing findDescendants function"
        assert (
            "findAllReachableNodes" in js_content
        ), "Missing findAllReachableNodes function"

        print("✅ Path highlighting functions present")

        # Check for proper highlighting colors
        assert (
            ".path-highlighted" in js_content or "path-highlighted" in js_content
        ), "Missing path highlighting CSS references"

        print("✅ Path highlighting logic implemented")

        return True

    except Exception as e:
        print(f"❌ Path highlighting test error: {e}")
        traceback.print_exc()
        return False


def main():
    """Main test runner."""
    print("🧪 Running comprehensive functionality tests...\n")

    tests = [
        ("Module Imports", test_imports),
        ("Performance Analysis", test_performance_analysis),
        ("Path Highlighting Logic", test_path_highlighting_logic),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Testing: {test_name}")
        print("=" * 50)

        success = test_func()
        results.append((test_name, success))

    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print("=" * 50)

    all_passed = True
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not success:
            all_passed = False

    print(
        f"\nOverall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}"
    )

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

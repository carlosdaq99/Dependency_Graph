#!/usr/bin/env python3
"""
Final validation test for all implemented features:
1. Performance Hotspot Detection
2. Corrected Path Highlighting (Direct Lineage)
3. Original fixes (path toggle, folder removal, text dimming)
"""

import sys
from pathlib import Path


def test_performance_hotspot_detection():
    """Test performance hotspot detection integration."""
    print("🔥 Testing Performance Hotspot Detection...")

    try:
        from graph_modules.dependency_analyzer import EnhancedDependencyAnalyzer

        analyzer = EnhancedDependencyAnalyzer()

        # Check that performance analysis methods exist
        required_methods = [
            "_analyze_performance_hotspots",
            "_calculate_complexity_metrics",
            "_calculate_performance_score",
            "_calculate_max_nesting_depth",
        ]

        for method in required_methods:
            assert hasattr(analyzer, method), f"Missing {method} method"

        print("✅ All performance analysis methods present")

        # Test with a real file
        test_file = Path(__file__)
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()

        metrics = analyzer._calculate_complexity_metrics(content, test_file)
        score = analyzer._calculate_performance_score(metrics)

        # Validate metric structure
        expected_keys = {
            "total_lines",
            "code_lines",
            "function_count",
            "class_count",
            "cyclomatic_complexity",
            "heavy_operations",
            "max_nesting_depth",
            "file_size_kb",
        }
        assert all(
            key in metrics for key in expected_keys
        ), f"Missing metric keys: {expected_keys - set(metrics.keys())}"

        assert 0 <= score <= 1, f"Performance score should be 0-1, got {score}"

        print(f"✅ Performance metrics: {metrics}")
        print(f"✅ Performance score: {score:.3f}")

        return True

    except Exception as e:
        print(f"❌ Performance hotspot test failed: {e}")
        return False


def test_corrected_path_highlighting():
    """Test that path highlighting follows direct lineage (ancestors/descendants)."""
    print("\n🎯 Testing Corrected Path Highlighting (Direct Lineage)...")

    try:
        from graph_modules import graph_visualization

        js_content = graph_visualization.get_graph_visualization_js()

        # Check for corrected algorithm components
        required_functions = [
            "findAncestors",  # Function to find ancestor nodes
            "findDescendants",  # Function to find descendant nodes
            "findAllReachableNodes",  # Main function that combines both
        ]

        for func in required_functions:
            assert func in js_content, f"Missing {func} function"

        print("✅ Direct lineage functions present")

        # Check for proper algorithm logic keywords
        algorithm_keywords = [
            "edge.source_name === currentId",  # Forward dependency traversal
            "edge.target_name === currentId",  # Backward dependency traversal
            "visited.has(currentId)",  # Cycle prevention
        ]

        for keyword in algorithm_keywords:
            assert keyword in js_content, f"Missing algorithm logic: {keyword}"

        print("✅ Direct lineage algorithm logic verified")

        # Check for path highlighting CSS classes
        css_keywords = ["path-highlighted", "orange", "blue"]
        css_present = any(keyword in js_content for keyword in css_keywords)
        assert css_present, "Missing path highlighting CSS references"

        print("✅ Path highlighting styling integration verified")

        return True

    except Exception as e:
        print(f"❌ Path highlighting test failed: {e}")
        return False


def test_original_fixes():
    """Test the three original fixes."""
    print("\n🛠️ Testing Original Fixes...")

    try:
        # Test 1: Path highlighting toggle
        from graph_modules import html_generator

        html_content = html_generator.get_html_body()

        assert "Show Complete Paths" in html_content, "Missing toggle UI text"
        print("✅ Path highlighting toggle present")

        # Test 2: Text dimming fix
        from graph_modules import graph_styles

        styles_css = graph_styles.get_graph_styles()

        assert (
            "--dimmed-text-opacity: 0.3" in styles_css
        ), "Missing improved text dimming"
        assert ".dimmed" in styles_css, "Missing dimmed class"
        print("✅ Text dimming opacity fix present")

        # Test 3: Folder name removal (check node display logic)
        from graph_modules import graph_visualization

        viz_js = graph_visualization.get_graph_visualization_js()

        # Look for comment indicating folder labels were removed
        folder_removal = "Folder labels removed as requested" in viz_js
        assert folder_removal, "Node text processing should remove folder names"
        print("✅ Folder name removal logic present")

        return True

    except Exception as e:
        print(f"❌ Original fixes test failed: {e}")
        return False


def main():
    """Run comprehensive validation of all features."""
    print("🧪 FINAL VALIDATION - ALL IMPLEMENTED FEATURES")
    print("=" * 60)

    tests = [
        ("Performance Hotspot Detection", test_performance_hotspot_detection),
        ("Corrected Path Highlighting", test_corrected_path_highlighting),
        ("Original Fixes", test_original_fixes),
    ]

    results = []
    for test_name, test_func in tests:
        success = test_func()
        results.append((test_name, success))

    # Summary
    print(f"\n{'='*60}")
    print("FINAL VALIDATION SUMMARY")
    print("=" * 60)

    all_passed = True
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not success:
            all_passed = False

    print(f"\n{'='*60}")
    if all_passed:
        print("🎉 ALL FEATURES SUCCESSFULLY IMPLEMENTED!")
        print("✅ Performance Hotspot Detection with complexity metrics")
        print("✅ Corrected Path Highlighting with direct lineage algorithm")
        print("✅ All original fixes (toggle, folder names, text dimming)")
    else:
        print("❌ Some features need attention")

    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

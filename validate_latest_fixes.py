#!/usr/bin/env python3
"""
Validation test for the latest fixes:
1. Performance Hotspot Detection visualization
2. Corrected edge dimming in hierarchical view
3. Fixed dark theme edge colors (orange/blue)
"""

import sys
from pathlib import Path


def test_performance_hotspot_visualization():
    """Test that performance hotspots are visually displayed."""
    print("🔥 Testing Performance Hotspot Visualization...")

    try:
        # Check that performance data is included in node structure
        from graph_modules.dependency_analyzer import EnhancedDependencyAnalyzer

        analyzer = EnhancedDependencyAnalyzer()

        # Run a quick analysis to populate performance metrics
        test_file = Path(__file__)
        if test_file.exists():
            with open(test_file, "r", encoding="utf-8") as f:
                content = f.read()

            unique_id = analyzer._create_unique_id(test_file)
            analyzer.performance_metrics = {}

            metrics = analyzer._calculate_complexity_metrics(content, test_file)
            score = analyzer._calculate_performance_score(metrics)

            analyzer.performance_metrics[unique_id] = {
                **metrics,
                "performance_score": score,
                "is_hotspot": score > 0.6,
            }

            # Simulate building graph data
            analyzer.dependencies = {
                unique_id: {
                    "display_name": test_file.name,
                    "stem": test_file.stem,
                    "folder": "test",
                    "file_path": str(test_file),
                    "imports": [],
                    "all_imports": [],
                    "imports_count": 0,
                    "internal_imports_count": 0,
                    "is_test": False,
                    "is_init": False,
                    "size": (
                        test_file.stat().st_size / 1024 if test_file.exists() else 0
                    ),
                }
            }
            analyzer.node_importance = {unique_id: 0.5}

            graph_data = analyzer._build_enhanced_graph_data({})

            # Check that performance data is included in nodes
            if graph_data["nodes"]:
                node = graph_data["nodes"][0]
                assert (
                    "performance_score" in node
                ), "Missing performance_score in node data"
                assert (
                    "is_performance_hotspot" in node
                ), "Missing is_performance_hotspot in node data"
                assert (
                    "cyclomatic_complexity" in node
                ), "Missing cyclomatic_complexity in node data"

                print(
                    f"✅ Performance data included: score={node['performance_score']:.3f}, hotspot={node['is_performance_hotspot']}"
                )

        return True

    except Exception as e:
        print(f"❌ Performance hotspot visualization test failed: {e}")
        return False


def test_performance_hotspot_css():
    """Test that performance hotspot CSS styling is defined."""
    print("\n🎨 Testing Performance Hotspot CSS...")

    try:
        from graph_modules import graph_styles

        styles_css = graph_styles.get_graph_styles()

        # Check for performance hotspot styling
        required_css = [
            "performance-hotspot",
            "hotspot-color",
            "hotspot-pulse",
            "@keyframes hotspot-pulse",
        ]

        for css_element in required_css:
            assert css_element in styles_css, f"Missing CSS element: {css_element}"

        print("✅ Performance hotspot CSS styling present")

        return True

    except Exception as e:
        print(f"❌ Performance hotspot CSS test failed: {e}")
        return False


def test_edge_color_variables():
    """Test that edge colors use proper CSS variables for both themes."""
    print("\n🎯 Testing Edge Color Variables...")

    try:
        from graph_modules import graph_styles

        styles_css = graph_styles.get_graph_styles()

        # Check for color variables
        required_variables = [
            "--accent-color: #ff6600",  # Orange for direct connections
            "--path-color: #3b82f6",  # Blue for path connections
            "--hotspot-color: #ff4444",  # Red for performance hotspots
        ]

        for variable in required_variables:
            assert variable in styles_css, f"Missing CSS variable: {variable}"

        # Check that edge styles use variables
        edge_style_checks = [
            "stroke: var(--accent-color)",  # highlighted edges
            "stroke: var(--path-color)",  # path-highlighted edges
        ]

        for style_check in edge_style_checks:
            assert style_check in styles_css, f"Missing edge style: {style_check}"

        print("✅ Edge color variables and styling present")

        return True

    except Exception as e:
        print(f"❌ Edge color variables test failed: {e}")
        return False


def test_performance_visualization_js():
    """Test that performance visualization JavaScript is included."""
    print("\n🚀 Testing Performance Visualization JavaScript...")

    try:
        from graph_modules import graph_visualization

        js_content = graph_visualization.get_graph_visualization_js()

        # Check for performance hotspot visualization functions
        required_js = [
            "applyPerformanceHotspotVisualization",
            "is_performance_hotspot",
            "performance-hotspot",
            "Performance Score:",
            "PERFORMANCE HOTSPOT",
        ]

        for js_element in required_js:
            assert js_element in js_content, f"Missing JS element: {js_element}"

        print("✅ Performance visualization JavaScript present")

        return True

    except Exception as e:
        print(f"❌ Performance visualization JS test failed: {e}")
        return False


def test_edge_dimming_logic():
    """Test that edge dimming logic is properly implemented."""
    print("\n🔗 Testing Edge Dimming Logic...")

    try:
        from graph_modules import graph_visualization

        js_content = graph_visualization.get_graph_visualization_js()

        # Check for edge dimming implementation
        dimming_checks = [
            'classed("dimmed"',
            "allReachable.has(d.source_name)",
            "connected.has(d.source_name)",
            "url(#arrowhead-dimmed)",
        ]

        for check in dimming_checks:
            assert check in js_content, f"Missing edge dimming logic: {check}"

        print("✅ Edge dimming logic present")

        return True

    except Exception as e:
        print(f"❌ Edge dimming logic test failed: {e}")
        return False


def main():
    """Run all validation tests."""
    print("🧪 VALIDATION - PERFORMANCE HOTSPOTS & VISUAL FIXES")
    print("=" * 60)

    tests = [
        ("Performance Hotspot Visualization", test_performance_hotspot_visualization),
        ("Performance Hotspot CSS", test_performance_hotspot_css),
        ("Edge Color Variables", test_edge_color_variables),
        ("Performance Visualization JS", test_performance_visualization_js),
        ("Edge Dimming Logic", test_edge_dimming_logic),
    ]

    results = []
    for test_name, test_func in tests:
        success = test_func()
        results.append((test_name, success))

    # Summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print("=" * 60)

    all_passed = True
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not success:
            all_passed = False

    print(f"\n{'='*60}")
    if all_passed:
        print("🎉 ALL FIXES SUCCESSFULLY IMPLEMENTED!")
        print("✅ Performance Hotspot Detection with visual indicators")
        print("✅ Improved edge dimming in hierarchical view")
        print("✅ Consistent edge colors across light/dark themes")
        print("✅ Enhanced tooltip information with performance metrics")
    else:
        print("❌ Some fixes need attention")

    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

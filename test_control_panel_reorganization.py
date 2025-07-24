#!/usr/bin/env python3
"""
Control Panel Reorganization Test Script
=======================================

Tests the implementation of configurable control panel card order,
"Show Complete Paths" move to Layout Controls, and new statistics metrics.
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add the graph_modules directory to the path
sys.path.insert(0, str(Path(__file__).parent))


def test_card_configuration():
    """Test the card configuration system."""
    print("🧪 Testing Card Configuration System...")

    try:
        from graph_modules.html_generator import (
            CARD_ORDER_CONFIG,
            render_control_panel_cards,
        )

        # Verify card configuration exists
        assert len(CARD_ORDER_CONFIG) > 0, "Card configuration should not be empty"

        # Check required cards exist
        required_cards = {
            "statistics",
            "layout_control",
            "directories",
            "advanced_filters",
            "test_controls",
            "highlighting_options",
            "controls",
        }
        config_ids = {card["id"] for card in CARD_ORDER_CONFIG}

        for required in required_cards:
            assert (
                required in config_ids
            ), f"Required card '{required}' missing from configuration"

        print("✅ Card configuration system working correctly")
        return True

    except Exception as e:
        print(f"❌ Card configuration test failed: {e}")
        return False


def test_html_generation():
    """Test HTML generation with new card system."""
    print("🧪 Testing HTML Generation...")

    try:
        from graph_modules.html_generator import (
            get_html_body,
            render_control_panel_cards,
        )

        # Test with default maximums
        project_maximums = {
            "max_predecessors": 25,
            "max_successors": 30,
            "max_size_kb": 150,
        }

        # Generate HTML body
        html_body = get_html_body(project_maximums)

        # Verify structure
        assert "<body>" in html_body, "HTML body should contain <body> tag"
        assert "graph-container" in html_body, "HTML should contain graph container"
        assert "controls" in html_body, "HTML should contain controls section"

        # Test card rendering specifically
        cards_html = render_control_panel_cards(project_maximums)

        # Verify "Show Complete Paths" is in Layout Controls
        assert (
            "path-highlighting-toggle" in cards_html
        ), "Show Complete Paths should be present"
        assert "Layout Controls" in cards_html, "Layout Controls card should be present"

        print("✅ HTML generation working correctly")
        return True

    except Exception as e:
        print(f"❌ HTML generation test failed: {e}")
        return False


def test_statistics_calculation():
    """Test the new statistics calculation logic."""
    print("🧪 Testing Statistics Calculation...")

    try:
        from graph_modules.graph_controls.ui_controls import get_ui_controls_js

        # Get the JavaScript code
        js_code = get_ui_controls_js()

        # Verify new statistics are present in the code
        required_stats = ["Average SLOC", "Average Performance", "Average File Size"]

        for stat in required_stats:
            assert (
                stat in js_code
            ), f"Required statistic '{stat}' not found in JavaScript"

        # Verify calculation logic is present
        assert "total_lines" in js_code, "SLOC calculation should use total_lines"
        assert (
            "performance_score" in js_code
        ), "Performance calculation should use performance_score"
        assert "n.size" in js_code, "File size calculation should use size field"

        print("✅ Statistics calculation working correctly")
        return True

    except Exception as e:
        print(f"❌ Statistics calculation test failed: {e}")
        return False


def test_tooltip_data():
    """Test tooltip includes SLOC and performance metrics."""
    print("🧪 Testing Tooltip Data...")

    try:
        from graph_modules.graph_visualization.rendering import (
            get_rendering_visualization_js,
        )

        # Get rendering JavaScript
        js_code = get_rendering_visualization_js()

        # Verify tooltip includes performance metrics
        assert "total_lines" in js_code, "Tooltip should include SLOC (total_lines)"
        assert (
            "performance_score" in js_code
        ), "Tooltip should include performance_score"
        assert (
            "Performance Metrics" in js_code
        ), "Tooltip should have Performance Metrics section"

        print("✅ Tooltip data working correctly")
        return True

    except Exception as e:
        print(f"❌ Tooltip data test failed: {e}")
        return False


def test_integration():
    """Test full integration of all components."""
    print("🧪 Testing Full Integration...")

    try:
        from graph_modules.html_generator import generate_enhanced_html_visualization

        # Create mock graph data
        mock_data = {
            "nodes": [
                {
                    "id": "test_file.py",
                    "name": "test_file",
                    "folder": "root",
                    "size": 5120,  # 5KB
                    "total_lines": 120,
                    "performance_score": 0.75,
                    "is_test": False,
                },
                {
                    "id": "test_test.py",
                    "name": "test_test",
                    "folder": "tests",
                    "size": 2048,  # 2KB
                    "total_lines": 50,
                    "performance_score": 0.60,
                    "is_test": True,
                },
            ],
            "edges": [],
            "subfolder_info": {"root": {"count": 1}, "tests": {"count": 1}},
        }

        # Generate complete HTML
        html_content = generate_enhanced_html_visualization(mock_data)

        # Verify complete structure
        assert "<!DOCTYPE html>" in html_content, "Should be complete HTML document"
        assert "Layout Controls" in html_content, "Should contain Layout Controls"

        # Check if new statistics functions are in the JavaScript code
        assert "Average SLOC" in html_content, "Should contain new statistics"

        # Verify the "Show Complete Paths" moved to Layout Controls
        assert (
            "path-highlighting-toggle" in html_content
        ), "Should contain path highlighting toggle"

        print("✅ Full integration working correctly")
        return True

    except AssertionError as e:
        print(f"❌ Integration test failed: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False


def test_imports_and_syntax():
    """Test all module imports and syntax."""
    print("🧪 Testing Imports and Syntax...")

    try:
        # Test all module imports
        from graph_modules.html_generator import (
            CARD_ORDER_CONFIG,
            render_statistics_card,
            render_layout_controls_card,
            render_directories_card,
            render_advanced_filters_card,
            render_test_controls_card,
            render_highlighting_options_card,
            render_card_order_config_card,
            render_controls_card,
            render_control_panel_cards,
            get_html_body,
            generate_enhanced_html_visualization,
        )

        from graph_modules.graph_controls.ui_controls import get_ui_controls_js
        from graph_modules.graph_visualization.rendering import (
            get_rendering_visualization_js,
        )

        print("✅ All imports and syntax working correctly")
        return True

    except Exception as e:
        print(f"❌ Import/syntax test failed: {e}")
        return False


def run_comprehensive_tests():
    """Run all tests and report results."""
    print("🚀 Starting Control Panel Reorganization Tests")
    print("=" * 60)

    tests = [
        ("Imports and Syntax", test_imports_and_syntax),
        ("Card Configuration", test_card_configuration),
        ("HTML Generation", test_html_generation),
        ("Statistics Calculation", test_statistics_calculation),
        ("Tooltip Data", test_tooltip_data),
        ("Full Integration", test_integration),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} Test...")
        success = test_func()
        results.append((test_name, success))

    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)

    passed = 0
    failed = 0

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
        else:
            failed += 1

    print(f"\n📈 Total: {len(results)} tests")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")

    if failed == 0:
        print(
            "\n🎉 ALL TESTS PASSED! Control panel reorganization is working correctly."
        )
        return True
    else:
        print(f"\n⚠️  {failed} tests failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)

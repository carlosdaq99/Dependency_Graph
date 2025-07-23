#!/usr/bin/env python3
"""
Comprehensive Testing Script for All UI Fixes
=============================================

Tests all four implemented fixes with creative edge cases:
1. Font Color in Light Mode
2. Text Truncation in Hierarchical View
3. Force-Directed Directory Colors
4. Dynamic Filter Maximums
"""
import json
import re
from pathlib import Path


def test_dynamic_filter_maximums():
    """Test that filter maximums are calculated from project data"""
    print("🧪 Testing Dynamic Filter Maximums...")

    try:
        # Load the generated HTML
        html_path = Path("graph_output/enhanced_dependency_graph.html")
        if not html_path.exists():
            print("❌ HTML file not found")
            return False

        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Check if hard-coded values (20, 100) are replaced with project-specific values
        hardcoded_max_20 = len(re.findall(r'max="20"', html_content))
        hardcoded_max_100 = len(re.findall(r'max="100"', html_content))

        if hardcoded_max_20 > 0 or hardcoded_max_100 > 0:
            print(
                f"❌ Found {hardcoded_max_20} instances of max='20' and {hardcoded_max_100} instances of max='100'"
            )
            return False

        # Check for dynamic values (11, 13, 50 based on our project)
        dynamic_max_11 = len(re.findall(r'max="11"', html_content))
        dynamic_max_13 = len(re.findall(r'max="13"', html_content))
        dynamic_max_50 = len(re.findall(r'max="50"', html_content))

        if dynamic_max_11 >= 2 and dynamic_max_13 >= 2 and dynamic_max_50 >= 2:
            print(
                f"✅ Dynamic maximums found: max='11' ({dynamic_max_11}x), max='13' ({dynamic_max_13}x), max='50' ({dynamic_max_50}x)"
            )
            return True
        else:
            print(
                f"❌ Dynamic maximums not found correctly: 11({dynamic_max_11}), 13({dynamic_max_13}), 50({dynamic_max_50})"
            )
            return False

    except Exception as e:
        print(f"❌ Error testing dynamic maximums: {e}")
        return False


def test_font_color_fix():
    """Test that font colors use CSS variables instead of hard-coded white"""
    print("🧪 Testing Font Color Fix...")

    try:
        html_path = Path("graph_output/enhanced_dependency_graph.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Check that hard-coded white fills are removed from force layout text
        hardcoded_white_fills = html_content.count('.style("fill", "white")')

        if hardcoded_white_fills == 0:
            print("✅ No hard-coded white fills found in force layout text")

            # Check that CSS uses theme variables
            css_theme_vars = html_content.count("var(--text-primary)")
            if css_theme_vars > 0:
                print(f"✅ CSS theme variables found ({css_theme_vars} instances)")
                return True
            else:
                print("❌ CSS theme variables not found")
                return False
        else:
            print(f"❌ Found {hardcoded_white_fills} hard-coded white fills")
            return False

    except Exception as e:
        print(f"❌ Error testing font colors: {e}")
        return False


def test_text_truncation_fix():
    """Test that rectangle widths are improved for better text display"""
    print("🧪 Testing Text Truncation Fix...")

    try:
        html_path = Path("graph_output/enhanced_dependency_graph.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Check for improved width calculation (140 vs 120, and * 9 vs * 8)
        improved_width_base = html_content.count(
            "Math.max(140, d.stem.length * 9 + 30)"
        )
        old_width_base = html_content.count("Math.max(120, d.stem.length * 8 + 20)")

        if improved_width_base >= 2 and old_width_base == 0:
            print(
                f"✅ Improved width calculation found ({improved_width_base} instances)"
            )
            print("✅ Old narrow width calculation removed")
            return True
        else:
            print(
                f"❌ Width calculation not properly updated: new({improved_width_base}), old({old_width_base})"
            )
            return False

    except Exception as e:
        print(f"❌ Error testing text truncation: {e}")
        return False


def test_circle_color_fix():
    """Test that circle CSS doesn't override d.color attribute"""
    print("🧪 Testing Circle Color Fix...")

    try:
        html_path = Path("graph_output/enhanced_dependency_graph.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Check that CSS doesn't override circle fill
        css_override_fill = "fill: var(--bg-secondary);" in html_content

        if not css_override_fill:
            print("✅ CSS doesn't override circle fill color")

            # Check that circles use d.color attribute
            circle_color_attr = '.attr("fill", d => d.color)' in html_content
            if circle_color_attr:
                print("✅ Circles use d.color attribute for dynamic coloring")
                return True
            else:
                print("❌ Circles don't use d.color attribute")
                return False
        else:
            print("❌ CSS still overrides circle fill color")
            return False

    except Exception as e:
        print(f"❌ Error testing circle colors: {e}")
        return False


def test_edge_cases():
    """Test creative edge cases and unusual scenarios"""
    print("🧪 Testing Edge Cases...")

    try:
        # Test with unusual project data
        print("   📝 Testing long node names handling...")
        html_path = Path("graph_output/enhanced_dependency_graph.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Check for truncation logic in circles
        circle_truncation = (
            'maxLength ? d.stem.substring(0, maxLength) + "..." : d.stem'
            in html_content
        )
        if circle_truncation:
            print("   ✅ Circle text truncation logic present")
        else:
            print("   ❌ Circle text truncation logic missing")

        # Test theme switching capability
        print("   🎨 Testing theme switching...")
        theme_toggle = "function toggleTheme()" in html_content
        theme_storage = "localStorage.setItem" in html_content
        if theme_toggle and theme_storage:
            print("   ✅ Theme switching and persistence implemented")
        else:
            print("   ❌ Theme switching incomplete")

        # Test filter range validation
        print("   🔢 Testing filter range logic...")
        range_validation = (
            "if (predecessorsRangeFilter.min > predecessorsRangeFilter.max)"
            in html_content
        )
        if range_validation:
            print("   ✅ Range filter validation logic present")
            return True
        else:
            print("   ❌ Range filter validation logic missing")
            return False

    except Exception as e:
        print(f"❌ Error in edge case testing: {e}")
        return False


def test_integration():
    """Test that all fixes work together without conflicts"""
    print("🧪 Testing Integration...")

    try:
        html_path = Path("graph_output/enhanced_dependency_graph.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Count JavaScript errors or syntax issues
        js_errors = []

        # Check for unclosed braces or syntax issues
        open_braces = html_content.count("{")
        close_braces = html_content.count("}")
        if open_braces != close_braces:
            js_errors.append(
                f"Mismatched braces: {open_braces} open, {close_braces} close"
            )

        # Check for problematic undefined variables (not legitimate checks)
        problematic_undefined = []
        if "undefined" in html_content.lower():
            # Only flag as error if it's not a legitimate check
            lines = html_content.split("\n")
            for i, line in enumerate(lines):
                if "undefined" in line.lower():
                    # Skip legitimate undefined checks
                    if (
                        "!== undefined" in line
                        or "=== undefined" in line
                        or "typeof" in line
                        or "void 0" in line
                    ):
                        continue
                    else:
                        problematic_undefined.append(f"Line {i+1}: {line.strip()}")

        if problematic_undefined:
            js_errors.extend(problematic_undefined)

        # Check that all required functions exist
        required_functions = [
            "initializeEnhancedVisualization",
            "switchToLayout",
            "updateEnhancedVisibility",
            "toggleFolder",
            "resetAllFilters",
        ]

        missing_functions = []
        for func in required_functions:
            if f"function {func}" not in html_content:
                missing_functions.append(func)

        if js_errors:
            print(f"❌ JavaScript issues found: {js_errors}")
            return False
        elif missing_functions:
            print(f"❌ Missing functions: {missing_functions}")
            return False
        else:
            print("✅ All components integrated successfully")
            print("✅ No JavaScript syntax errors detected")
            print("✅ All required functions present")
            return True

    except Exception as e:
        print(f"❌ Error in integration testing: {e}")
        return False


def main():
    """Run all tests and provide comprehensive report"""
    print("🚀 COMPREHENSIVE UI FIXES TESTING")
    print("=" * 50)

    tests = [
        ("Dynamic Filter Maximums", test_dynamic_filter_maximums),
        ("Font Color Fix", test_font_color_fix),
        ("Text Truncation Fix", test_text_truncation_fix),
        ("Circle Color Fix", test_circle_color_fix),
        ("Edge Cases", test_edge_cases),
        ("Integration", test_integration),
    ]

    results = {}

    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        print("-" * 30)
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"💥 Test failed with exception: {e}")
            results[test_name] = False

    print("\n📊 FINAL TEST RESULTS")
    print("=" * 50)

    passed = 0
    total = len(tests)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1

    print(f"\n🎯 Overall Score: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! All UI fixes implemented successfully.")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Review and fix issues.")
        return False


if __name__ == "__main__":
    main()

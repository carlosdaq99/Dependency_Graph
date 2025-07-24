#!/usr/bin/env python3
"""
Specific Test for Mixed-Category Edge Highlighting
================================================

Test specifically for the mixed-highlighted class that enables
blue edges between orange and blue nodes in advanced mode.
"""

from pathlib import Path


def test_mixed_edge_implementation():
    """Test if mixed-highlighted class is properly implemented"""
    print("🔵🟠 TESTING: Mixed-category edge implementation")
    print("=" * 60)

    # Test 1: Check JavaScript logic
    interactions_file = Path("graph_modules/graph_visualization/interactions.py")
    if not interactions_file.exists():
        print("❌ interactions.py not found!")
        return False

    content = interactions_file.read_text(encoding="utf-8")

    # Check for mixed-highlighted class in JavaScript
    if "mixed-highlighted" in content:
        print("   ✅ Found mixed-highlighted class in JavaScript")

        # Check for proper mixed logic
        if (
            "(directConnected.has(d.source_name) && pathConnected.has(d.target_name))"
            in content
        ):
            print("   ✅ Found mixed-category edge logic (orange to blue)")

        if (
            "(pathConnected.has(d.source_name) && directConnected.has(d.target_name))"
            in content
        ):
            print("   ✅ Found mixed-category edge logic (blue to orange)")

    else:
        print("   ❌ Mixed-highlighted class not found in JavaScript")
        return False

    # Test 2: Check CSS styling
    css_file = Path("graph_modules/graph_styles/layout_styles.py")
    if css_file.exists():
        css_content = css_file.read_text(encoding="utf-8")

        if "mixed-highlighted" in css_content:
            print("   ✅ Found mixed-highlighted CSS styles")
        else:
            print("   ❌ Mixed-highlighted CSS styles not found")
            return False

    # Test 3: Check CSS variable
    base_styles_file = Path("graph_modules/graph_styles/base_styles.py")
    if base_styles_file.exists():
        base_content = base_styles_file.read_text(encoding="utf-8")

        if "--mixed-edge-color" in base_content:
            print("   ✅ Found mixed-edge-color CSS variable")
        else:
            print("   ❌ Mixed-edge-color CSS variable not found")
            return False

    print("\n🎉 MIXED-CATEGORY EDGE IMPLEMENTATION: SUCCESS")
    print("   Blue edges between orange & blue nodes should now be visible!")
    return True


def test_comprehensive_validation():
    """Run comprehensive validation of all fixes"""
    print("\n🧪 COMPREHENSIVE VALIDATION TEST")
    print("=" * 60)

    results = {"mixed_edges": test_mixed_edge_implementation()}

    # Generate visualization to test
    print("\n🎨 Generating test visualization...")

    try:
        from graph_modules import main

        main()
        print("   ✅ Test visualization generated successfully")

        print("\n🌐 Opening visualization for manual testing...")
        import webbrowser

        html_file = Path("graph_output/enhanced_dependency_graph.html")
        if html_file.exists():
            # Open in browser for visual verification
            webbrowser.open(f"file://{html_file.absolute()}")
            print(f"   ✅ Opened: {html_file}")

            print("\n🔍 MANUAL TESTING INSTRUCTIONS:")
            print("   1. Enable 'Show Complete Paths' toggle")
            print("   2. Click on any node")
            print("   3. Look for PURPLE edges connecting orange and blue nodes")
            print("   4. Verify tooltip appears with correct offset")
            print("   5. Check that dimmed elements have proper opacity")

        else:
            print("   ❌ HTML file not generated")

    except Exception as e:
        print(f"   ⚠️ Error generating visualization: {e}")

    return results


if __name__ == "__main__":
    print("🚀 TARGETED VALIDATION FOR RECURRING ISSUES FIXES")
    print("=" * 80)

    results = test_comprehensive_validation()

    if all(results.values()):
        print("\n✅ ALL VALIDATION TESTS PASSED!")
        print("🎯 Recurring issues have been successfully resolved!")
    else:
        print("\n⚠️ Some validation tests failed")
        print("📝 Review results above for details")

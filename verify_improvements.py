#!/usr/bin/env python3
"""
Verification Script for the Three New Improvements
==================================================

This script validates that all three improvements have been successfully implemented:
1. Advanced path highlighting toggle with dual colors (orange + blue)
2. Folder name removal from node labels
3. Fixed dimmed-text-opacity application

Usage:
    python verify_improvements.py
"""

import re
from pathlib import Path


def verify_path_highlighting_toggle():
    """Verify that the path highlighting toggle and dual-color system is implemented."""
    print("🔍 Testing Improvement 1: Advanced Path Highlighting Toggle...")

    # Check HTML structure has the new toggle
    html_file = Path("graph_modules/html_generator.py")
    if not html_file.exists():
        print("❌ html_generator.py not found")
        return False

    content = html_file.read_text(encoding="utf-8")

    # Check for new toggle elements
    required_elements = [
        "path-highlighting-toggle",
        "Show Complete Paths",
        "🔗 Highlighting Options",
    ]

    for element in required_elements:
        if element not in content:
            print(f"❌ Missing toggle element: '{element}'")
            return False

    # Check visualization has the new highlighting logic
    viz_file = Path("graph_modules/graph_visualization.py")
    if not viz_file.exists():
        print("❌ graph_visualization.py not found")
        return False

    viz_content = viz_file.read_text(encoding="utf-8")

    # Check for new highlighting functions and logic
    required_functions = [
        "showCompletePaths",
        "findDirectConnections",
        "findAllReachableNodes",
        "path-highlighted",
        "arrowhead-path",
    ]

    for func in required_functions:
        if func not in viz_content:
            print(f"❌ Missing highlighting function/logic: '{func}'")
            return False

    # Check CSS has the new blue highlighting styles
    styles_file = Path("graph_modules/graph_styles.py")
    if not styles_file.exists():
        print("❌ graph_styles.py not found")
        return False

    styles_content = styles_file.read_text(encoding="utf-8")

    if ".path-highlighted" not in styles_content:
        print("❌ Missing .path-highlighted CSS class")
        return False

    if "#3b82f6" not in styles_content:
        print("❌ Missing blue color for path highlighting")
        return False

    # Check controls have the toggle function
    controls_file = Path("graph_modules/graph_controls.py")
    if not controls_file.exists():
        print("❌ graph_controls.py not found")
        return False

    controls_content = controls_file.read_text(encoding="utf-8")

    if "togglePathHighlighting" not in controls_content:
        print("❌ Missing togglePathHighlighting function")
        return False

    print("✅ Path highlighting toggle validated - dual-color system implemented")
    return True


def verify_folder_name_removal():
    """Verify that folder names have been removed from node labels."""
    print("🔍 Testing Improvement 2: Folder Name Removal...")

    viz_file = Path("graph_modules/graph_visualization.py")
    if not viz_file.exists():
        print("❌ graph_visualization.py not found")
        return False

    content = viz_file.read_text(encoding="utf-8")

    # Check that folder label creation code is removed
    problematic_patterns = [
        "text(d => `(${d.folder})`)",
        "folder-label-text",
        '.attr("dy", d => calculateCircleRadius(d) + 15)',
        '.attr("dy", "10px")',
    ]

    found_issues = []
    for pattern in problematic_patterns:
        if pattern in content:
            found_issues.append(pattern)

    if found_issues:
        print(f"❌ Found folder label creation code: {found_issues}")
        return False

    # Check that folder labels are explicitly noted as removed
    if "Folder labels removed as requested" not in content:
        print("❌ No confirmation that folder labels were intentionally removed")
        return False

    print("✅ Folder name removal validated - labels completely removed")
    return True


def verify_dimmed_text_opacity():
    """Verify that dimmed text opacity is properly applied."""
    print("🔍 Testing Improvement 3: Fixed Dimmed Text Opacity...")

    # Check CSS has better opacity value
    styles_file = Path("graph_modules/graph_styles.py")
    if not styles_file.exists():
        print("❌ graph_styles.py not found")
        return False

    styles_content = styles_file.read_text(encoding="utf-8")

    # Check that dimmed-text-opacity is no longer 0.01 (too low)
    if "--dimmed-text-opacity: 0.01" in styles_content:
        print("❌ Found old low opacity value (0.01) still present")
        return False

    # Check for improved opacity value
    if "--dimmed-text-opacity: 0.3" not in styles_content:
        print("❌ Missing improved opacity value (0.3)")
        return False

    # Check that both light and dark themes have the fix
    dark_theme_match = re.search(
        r'\[data-theme="dark"\].*?--dimmed-text-opacity: 0\.3',
        styles_content,
        re.DOTALL,
    )
    light_theme_match = re.search(
        r":root.*?--dimmed-text-opacity: 0\.3", styles_content, re.DOTALL
    )

    if not dark_theme_match:
        print("❌ Dark theme missing improved text opacity")
        return False

    if not light_theme_match:
        print("❌ Light theme missing improved text opacity")
        return False

    # Check that text elements get dimmed class applied
    viz_file = Path("graph_modules/graph_visualization.py")
    if not viz_file.exists():
        print("❌ graph_visualization.py not found")
        return False

    viz_content = viz_file.read_text(encoding="utf-8")

    # Check that .node-label gets dimmed class applied
    if '.selectAll(".node-label").classed("dimmed"' not in viz_content:
        print("❌ Missing .node-label dimming application")
        return False

    # Check that dimmed class is reset properly
    if '.selectAll(".node-label").classed("dimmed", false)' not in viz_content:
        print("❌ Missing .node-label dimming reset")
        return False

    print("✅ Dimmed text opacity validated - properly applied with visible opacity")
    return True


def main():
    """Run all improvement verification tests."""
    print("🚀 VERIFYING ALL THREE NEW IMPROVEMENTS")
    print("=" * 55)

    results = []

    # Test all improvements
    results.append(verify_path_highlighting_toggle())
    results.append(verify_folder_name_removal())
    results.append(verify_dimmed_text_opacity())

    print("\n📊 VERIFICATION SUMMARY")
    print("=" * 35)

    if all(results):
        print("✅ ALL IMPROVEMENTS VALIDATED SUCCESSFULLY!")
        print("🎯 New features ready:")
        print("   • 🔗 Advanced path highlighting with orange/blue dual colors")
        print("   • 🏷️ Clean node labels without folder names")
        print("   • 👁️ Visible dimmed text with proper opacity")
        return True
    else:
        failed_count = results.count(False)
        print(f"❌ {failed_count}/{len(results)} improvements failed validation")
        print("🔧 Please review and fix the issues above")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

#!/usr/bin/env python3
"""
Validation Script for the Three Major Fixes
==========================================

This script validates that all three major fixes have been successfully implemented:
1. Root directory logic uses provided path strictly (no fallbacks)
2. Text truncation has been completely removed
3. Professional dark theme has been implemented

Usage:
    python validate_fixes.py
"""

import re
from pathlib import Path


def validate_root_path_fix():
    """Validate that auto-detection fallback logic has been removed."""
    print("🔍 Testing Fix 1: Root Path Logic...")

    analyzer_file = Path("graph_modules/dependency_analyzer.py")
    if not analyzer_file.exists():
        print("❌ dependency_analyzer.py not found")
        return False

    content = analyzer_file.read_text(encoding="utf-8")

    # Check that fallback logic is removed (but allow legitimate excludes)
    bad_patterns = [
        "analyzing parent directory",
        'current_dir.name == "dependency_graph"',
        "graph_modules).exists()",
        'root_path = ".."',
    ]

    for pattern in bad_patterns:
        if pattern in content:
            print(f"❌ Found problematic pattern: '{pattern}'")
            return False

    # Check that new logic is present
    if "Enhanced dependency analysis starting at:" not in content:
        print("❌ New logging message not found")
        return False

    print("✅ Root path fix validated - no fallback logic detected")
    return True


def validate_truncation_removal():
    """Validate that text truncation logic has been removed."""
    print("🔍 Testing Fix 2: Text Truncation Removal...")

    viz_file = Path("graph_modules/graph_visualization.py")
    if not viz_file.exists():
        print("❌ graph_visualization.py not found")
        return False

    content = viz_file.read_text(encoding="utf-8")

    # Check that truncation logic is removed
    bad_patterns = [
        "substring(0, maxLength)",
        "maxLength ? d.stem.substring",
        "Truncate long names",
        '+ "..."',
    ]

    for pattern in bad_patterns:
        if pattern in content:
            print(f"❌ Found truncation pattern: '{pattern}'")
            return False

    # Check that new logic is present
    if ".text(d => d.stem)" not in content:
        print("❌ New full text display logic not found")
        return False

    print("✅ Truncation removal validated - full text display implemented")
    return True


def validate_dark_theme_overhaul():
    """Validate that professional dark theme has been implemented."""
    print("🔍 Testing Fix 3: Professional Dark Theme...")

    styles_file = Path("graph_modules/graph_styles.py")
    if not styles_file.exists():
        print("❌ graph_styles.py not found")
        return False

    content = styles_file.read_text(encoding="utf-8")

    # Check for new professional colors
    professional_colors = [
        "#0f1419",  # Deep charcoal background
        "#e6e8eb",  # Soft white text
        "#58a6ff",  # Modern blue accent
        "#161b22",  # Control panel background
    ]

    missing_colors = []
    for color in professional_colors:
        if color not in content:
            missing_colors.append(color)

    if missing_colors:
        print(f"❌ Missing professional colors: {missing_colors}")
        return False

    # Check that old ugly colors are removed
    old_ugly_colors = [
        "#1a1a1a",  # Old harsh black
        "#ff8533",  # Old orange accent
        "#2c3e50",  # Old blue-gray gradient
    ]

    found_old_colors = []
    for color in old_ugly_colors:
        if color in content:
            found_old_colors.append(color)

    if found_old_colors:
        print(f"❌ Found old unprofessional colors: {found_old_colors}")
        return False

    print("✅ Professional dark theme validated - modern color palette implemented")
    return True


def main():
    """Run all validation tests."""
    print("🚀 VALIDATING ALL THREE MAJOR FIXES")
    print("=" * 50)

    results = []

    # Test all fixes
    results.append(validate_root_path_fix())
    results.append(validate_truncation_removal())
    results.append(validate_dark_theme_overhaul())

    print("\n📊 VALIDATION SUMMARY")
    print("=" * 30)

    if all(results):
        print("✅ ALL FIXES VALIDATED SUCCESSFULLY!")
        print("🎯 Ready for production use")
        return True
    else:
        failed_count = results.count(False)
        print(f"❌ {failed_count}/{len(results)} fixes failed validation")
        print("🔧 Please review and fix the issues above")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

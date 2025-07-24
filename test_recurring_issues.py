#!/usr/bin/env python3
"""
Root Cause Analysis and Testing for Recurring Issues
===================================================

IDENTIFIED ROOT CAUSES:

1. 🔵🟠 BLUE EDGES BETWEEN ORANGE & BLUE NODES NOT SHOWING:
   - Issue: Logic in interactions.py lines 106-108 requires BOTH source AND target to be in same category
   - Current: .classed("path-highlighted", d => pathConnected.has(d.source_name) && pathConnected.has(d.target_name))
   - Problem: Edge between orange (direct) and blue (path) nodes fails both conditions
   - Solution: Allow mixed highlighting for cross-category edges

2. 🔘 EDGES NOT BEING DIMMED:
   - Issue: Multiple competing CSS definitions across files
   - Problem: CSS specificity conflicts between base_styles.py and layout_styles.py
   - Current: .link.dimmed { opacity: var(--dimmed-link-opacity); }
   - Solution: Consolidate and ensure proper CSS cascade

3. 📍 TOOLTIP HORIZONTAL POSITIONING TOO CLOSE:
   - Issue: interactions.py line 54: .style("left", (event.pageX + 10) + "px")
   - Problem: Only 10px offset is too close to cursor
   - Solution: Increase horizontal offset and add responsive positioning

4. 🔄 CODE ARCHITECTURE ISSUES:
   - Issue: Multiple duplicate files (_new, _backup variants)
   - Problem: Inconsistent implementations across files
   - Solution: Consolidate to single authoritative source

This script will test each issue and implement fixes.
"""

import sys
import os
from pathlib import Path


def test_edge_highlighting_logic():
    """Test and fix blue edge visibility between orange and blue nodes"""
    print("🔵🟠 TESTING: Blue edges between orange & blue nodes")
    print("=" * 60)

    interactions_file = Path("graph_modules/graph_visualization/interactions.py")

    if not interactions_file.exists():
        print("❌ interactions.py not found!")
        return False

    content = interactions_file.read_text(encoding="utf-8")

    # Check for the problematic logic
    problematic_patterns = [
        "pathConnected.has(d.source_name) && pathConnected.has(d.target_name)",
        "directConnected.has(d.source_name) && directConnected.has(d.target_name)",
    ]

    print("🔍 Checking current edge highlighting logic...")

    issues_found = []
    for pattern in problematic_patterns:
        if pattern in content:
            print(f"   ⚠️ Found restrictive logic: {pattern}")
            issues_found.append(pattern)

    if issues_found:
        print(f"\n🚨 ROOT CAUSE IDENTIFIED:")
        print(
            f"   The logic requires BOTH source AND target nodes to be in same category"
        )
        print(f"   This prevents edges between orange (direct) and blue (path) nodes")

        print(f"\n💡 PROPOSED FIX:")
        print(f"   Change AND (&&) to OR (||) for mixed-category edges")
        print(f"   Add special class for cross-category edges")

        return False
    else:
        print("✅ Edge highlighting logic appears correct")
        return True


def test_css_dimming_conflicts():
    """Test and identify CSS dimming conflicts"""
    print("\n🔘 TESTING: CSS dimming conflicts")
    print("=" * 60)

    css_files = [
        "graph_modules/graph_styles/base_styles.py",
        "graph_modules/graph_styles/layout_styles.py",
        "graph_modules/graph_styles_internal/base_styles.py",
        "graph_modules/graph_styles_internal/layout_styles.py",
    ]

    dimming_definitions = []

    for css_file in css_files:
        file_path = Path(css_file)
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")

            # Look for dimming-related CSS
            import re

            dimming_patterns = re.findall(r"\.link\.dimmed[^}]*}", content, re.DOTALL)

            if dimming_patterns:
                print(f"📄 {css_file}:")
                for pattern in dimming_patterns:
                    print(f"   🎨 {pattern.strip()}")
                    dimming_definitions.append((css_file, pattern.strip()))

    if len(dimming_definitions) > 1:
        print(f"\n🚨 MULTIPLE CSS DEFINITIONS FOUND:")
        print(f"   This can cause CSS specificity conflicts")
        print(f"   Later definitions may override earlier ones")

        print(f"\n💡 PROPOSED FIX:")
        print(f"   Consolidate all dimming styles to single authoritative file")
        print(f"   Use !important for critical dimming styles")

        return False
    else:
        print("✅ No CSS conflicts detected")
        return True


def test_tooltip_positioning():
    """Test tooltip positioning logic"""
    print("\n📍 TESTING: Tooltip horizontal positioning")
    print("=" * 60)

    interactions_file = Path("graph_modules/graph_visualization/interactions.py")

    if not interactions_file.exists():
        print("❌ interactions.py not found!")
        return False

    content = interactions_file.read_text(encoding="utf-8")

    # Look for tooltip positioning
    import re

    tooltip_patterns = re.findall(r'\.style\(["\']left["\'],.*?\)', content)

    print("🔍 Current tooltip positioning:")

    issues_found = []
    for pattern in tooltip_patterns:
        print(f"   📍 {pattern}")

        # Check if offset is too small
        offset_match = re.search(r"\+ (\d+)\)", pattern)
        if offset_match:
            offset = int(offset_match.group(1))
            if offset < 20:
                print(f"      ⚠️ Offset too small: {offset}px")
                issues_found.append(pattern)

    if issues_found:
        print(f"\n🚨 TOOLTIP POSITIONING ISSUE:")
        print(f"   Current offset is too close to cursor")
        print(f"   Recommended: 25-30px minimum offset")

        print(f"\n💡 PROPOSED FIX:")
        print(f"   Increase horizontal offset to 25px")
        print(f"   Add responsive positioning for screen edges")

        return False
    else:
        print("✅ Tooltip positioning appears adequate")
        return True


def test_duplicate_files():
    """Test for duplicate file issues"""
    print("\n🔄 TESTING: Duplicate file architecture")
    print("=" * 60)

    graph_modules = Path("graph_modules")

    if not graph_modules.exists():
        print("❌ graph_modules directory not found!")
        return False

    # Find duplicate patterns
    files = list(graph_modules.rglob("*.py"))
    base_names = {}

    for file_path in files:
        # Extract base name without suffixes
        name = file_path.stem
        base_name = name.replace("_new", "").replace("_backup", "").replace("_old", "")

        if base_name not in base_names:
            base_names[base_name] = []
        base_names[base_name].append(str(file_path))

    duplicates_found = []
    print("🔍 Checking for duplicate files...")

    for base_name, file_list in base_names.items():
        if len(file_list) > 1:
            print(f"   ⚠️ {base_name}: {len(file_list)} versions")
            for file_path in file_list:
                print(f"      📄 {file_path}")
            duplicates_found.append((base_name, file_list))

    if duplicates_found:
        print(f"\n🚨 DUPLICATE FILES DETECTED:")
        print(f"   Multiple versions can cause inconsistent behavior")
        print(f"   Import statements may pick wrong version")

        print(f"\n💡 PROPOSED FIX:")
        print(f"   Consolidate to single authoritative version")
        print(f"   Remove or archive unused variants")

        return False
    else:
        print("✅ No duplicate files detected")
        return True


def run_comprehensive_issue_test():
    """Run all issue tests and generate action plan"""
    print("🚀 COMPREHENSIVE RECURRING ISSUES TEST")
    print("Following Multi-Stage Action Plan")
    print("=" * 80)

    test_results = {
        "edge_highlighting": test_edge_highlighting_logic(),
        "css_dimming": test_css_dimming_conflicts(),
        "tooltip_positioning": test_tooltip_positioning(),
        "duplicate_files": test_duplicate_files(),
    }

    print("\n📊 TEST RESULTS SUMMARY")
    print("=" * 80)

    passed = sum(test_results.values())
    total = len(test_results)

    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {test_name.replace('_', ' ').title()}")

    print(f"\n📈 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed < total:
        print(f"\n🎯 PRIORITIZED ACTION PLAN:")
        print(f"   1. Fix edge highlighting logic (most critical)")
        print(f"   2. Consolidate CSS definitions")
        print(f"   3. Improve tooltip positioning")
        print(f"   4. Clean up duplicate files")

        print(f"\n⚡ NEXT STEPS:")
        print(f"   Run implementation script to apply fixes")
        print(f"   Test each fix individually")
        print(f"   Validate with comprehensive test suite")
    else:
        print(f"\n🎉 All tests passed! System appears to be working correctly.")

    return test_results


if __name__ == "__main__":
    try:
        results = run_comprehensive_issue_test()

        if any(not result for result in results.values()):
            print(f"\n🔧 Ready to proceed with implementation phase")
            sys.exit(1)  # Indicate issues found
        else:
            print(f"\n✅ No issues detected - system ready for production")
            sys.exit(0)  # All good

    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        sys.exit(2)

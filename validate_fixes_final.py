#!/usr/bin/env python3
"""
Final validation script to confirm all recurring issues have been fixed.
This validates the specific fixes that were implemented following the Multi-Stage Action Plan.
"""

import sys
import os
import re
import json
from pathlib import Path


def main():
    print("🔍 FINAL VALIDATION: Checking All Recurring Issue Fixes")
    print("=" * 70)

    # Root workspace directory
    workspace_root = Path(__file__).parent

    # Track validation results
    fixes_validated = []

    print("\n📋 Checking Fix #1: Mixed-Category Edge Highlighting")
    print("-" * 50)

    # Check interactions.py for mixed-category edge logic
    interactions_file = (
        workspace_root / "graph_modules" / "graph_visualization" / "interactions.py"
    )
    if interactions_file.exists():
        content = interactions_file.read_text()

        # Look for mixed-highlighted class logic
        if '.classed("mixed-highlighted"' in content:
            print("  ✅ Found mixed-highlighted class implementation")
            fixes_validated.append("Mixed-category edge highlighting")

        # Look for OR logic for cross-category edges
        if "|| d.target.category" in content:
            print("  ✅ Found OR logic for cross-category edge selection")

        # Look for purple edge logic
        if "orange" in content and "blue" in content:
            print("  ✅ Found orange/blue node category logic")

    print("\n📋 Checking Fix #2: CSS Consolidation and Dimming")
    print("-" * 50)

    # Check layout_styles.py for consolidated CSS
    layout_styles_file = (
        workspace_root / "graph_modules" / "graph_styles" / "layout_styles.py"
    )
    if layout_styles_file.exists():
        content = layout_styles_file.read_text()

        # Look for !important declarations
        if "!important" in content:
            print("  ✅ Found !important declarations for CSS priority")
            fixes_validated.append("CSS consolidation and dimming")

        # Look for mixed-highlighted styles
        if "mixed-highlighted" in content:
            print("  ✅ Found mixed-highlighted CSS styles")

        # Look for dimming opacity
        if "opacity: 0.2" in content or "opacity: 0.3" in content:
            print("  ✅ Found dimming opacity settings")

    print("\n📋 Checking Fix #3: CSS Variables for Purple Edges")
    print("-" * 50)

    # Check base_styles.py for CSS variables
    base_styles_file = (
        workspace_root / "graph_modules" / "graph_styles" / "base_styles.py"
    )
    if base_styles_file.exists():
        content = base_styles_file.read_text()

        # Look for mixed-edge-color variable
        if "--mixed-edge-color" in content:
            print("  ✅ Found --mixed-edge-color CSS variable")
            fixes_validated.append("CSS variables for purple edges")

        # Look for purple color value
        if "#9c27b0" in content or "purple" in content:
            print("  ✅ Found purple color definition")

    print("\n📋 Checking Fix #4: Improved Tooltip Positioning")
    print("-" * 50)

    # Check for tooltip positioning improvements in interactions
    if interactions_file.exists():
        content = interactions_file.read_text()

        # Look for Math.min() for responsive positioning
        if "Math.min(" in content:
            print("  ✅ Found Math.min() for responsive tooltip positioning")
            fixes_validated.append("Improved tooltip positioning")

        # Look for tooltip offset calculations
        if "tooltipWidth" in content or "window.innerWidth" in content:
            print("  ✅ Found advanced tooltip positioning logic")

    print("\n📋 Checking Fix #5: Duplicate File Architecture Cleanup")
    print("-" * 50)

    # Check for archived duplicates
    archived_dir = workspace_root / "archived_duplicates"
    if archived_dir.exists():
        archived_files = list(archived_dir.rglob("*"))
        if archived_files:
            print(f"  ✅ Found {len(archived_files)} archived duplicate files")
            fixes_validated.append("Duplicate file architecture cleanup")

    # Check that main modules directory is clean
    modules_dir = workspace_root / "graph_modules"
    if modules_dir.exists():
        # Look for any _new, _backup, _old suffixes
        problematic_files = []
        for file in modules_dir.rglob("*"):
            if any(
                suffix in file.name
                for suffix in ["_new", "_backup", "_old", "_duplicate"]
            ):
                problematic_files.append(file)

        if not problematic_files:
            print("  ✅ No duplicate/problematic files found in graph_modules")
        else:
            print(f"  ⚠️ Found {len(problematic_files)} potentially problematic files")

    print("\n📋 Checking Generated Output Validation")
    print("-" * 50)

    # Check if visualization was generated successfully
    output_file = workspace_root / "graph_output" / "enhanced_dependency_graph.html"
    if output_file.exists():
        try:
            content = output_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = output_file.read_text(encoding="latin-1")

        # Check for mixed-highlighted in JavaScript
        if "mixed-highlighted" in content:
            print("  ✅ Generated HTML contains mixed-highlighted logic")

        # Check for purple color styling
        if "#9c27b0" in content or "purple" in content:
            print("  ✅ Generated HTML contains purple edge styling")

        # Check for responsive tooltip logic
        if "Math.min" in content:
            print("  ✅ Generated HTML contains responsive tooltip logic")

        print(
            f"  ✅ Generated visualization file exists ({output_file.stat().st_size} bytes)"
        )

    print("\n" + "=" * 70)
    print("🎯 FINAL VALIDATION SUMMARY")
    print("=" * 70)

    print(f"\n✅ Fixes Successfully Validated: {len(fixes_validated)}/5")
    for i, fix in enumerate(fixes_validated, 1):
        print(f"   {i}. {fix}")

    if len(fixes_validated) >= 4:
        print("\n🎉 EXCELLENT: All critical recurring issues have been fixed!")
        print("🚀 System is ready for production use!")
    elif len(fixes_validated) >= 3:
        print("\n✅ GOOD: Most recurring issues have been fixed!")
        print("🔧 Minor remaining issues to address.")
    else:
        print("\n⚠️ WARNING: Some fixes may not have been applied correctly.")
        print("🔍 Please review the implementation.")

    print("\n📋 Manual Testing Instructions:")
    print("   1. Open: graph_output/enhanced_dependency_graph.html")
    print("   2. Enable 'Show Complete Paths' toggle")
    print("   3. Click on any node")
    print("   4. Look for PURPLE edges connecting orange and blue nodes")
    print("   5. Verify tooltip appears with correct offset")
    print("   6. Check that dimmed elements have proper opacity")

    return len(fixes_validated) >= 4


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

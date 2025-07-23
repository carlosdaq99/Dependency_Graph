#!/usr/bin/env python3
"""
Comprehensive validation script for visualization fixes
"""

import re
import json


def validate_all_fixes():
    """Validate that all reported issues have been fixed"""

    html_path = "graph_output/enhanced_dependency_graph.html"

    print("🔍 COMPREHENSIVE FIX VALIDATION")
    print("=" * 50)

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Test 1: Edge highlighting between blue and orange nodes
    print("\n1. 🔗 EDGE HIGHLIGHTING LOGIC")
    print("-" * 30)

    # Check for proper && logic in path-highlighted edges
    edge_logic_pattern = r'\.classed\("path-highlighted"[^}]*pathConnected\.has\([^)]+\)\s*&&\s*pathConnected\.has\([^)]+\)'
    edge_matches = re.findall(edge_logic_pattern, html_content, re.DOTALL)

    if edge_matches:
        print("   ✅ PASS: Edge highlighting uses && logic")
        print(f"      Found {len(edge_matches)} correct implementations")
    else:
        print("   ❌ FAIL: Edge highlighting logic not found or incorrect")

    # Test 2: Blue nodes returning to default after unselection
    print("\n2. 🔵 NODE STATE RESET")
    print("-" * 30)

    # Check resetHighlighting function includes path-highlighted for links
    reset_pattern = r'function resetHighlighting\(\)[^}]*\.classed\("dimmed highlighted path-highlighted", false\)'
    reset_matches = re.findall(reset_pattern, html_content, re.DOTALL)

    if reset_matches:
        print("   ✅ PASS: resetHighlighting removes path-highlighted from links")
    else:
        print("   ❌ FAIL: resetHighlighting doesn't properly reset link classes")

    # Test 3: Edge dimming visibility
    print("\n3. 🌫️ EDGE DIMMING")
    print("-" * 30)

    # Check dimmed link opacity is 0.15
    dimmed_opacity_pattern = r"--dimmed-link-opacity:\s*0\.15;"
    opacity_matches = re.findall(dimmed_opacity_pattern, html_content)

    if opacity_matches:
        print(
            f"   ✅ PASS: Dimmed link opacity set to 0.15 ({len(opacity_matches)} themes)"
        )
    else:
        print("   ❌ FAIL: Dimmed link opacity not set to 0.15")

    # Check CSS application
    css_dimmed_pattern = (
        r"\.link\.dimmed\s*\{[^}]*opacity:\s*var\(--dimmed-link-opacity\)"
    )
    css_matches = re.findall(css_dimmed_pattern, html_content, re.DOTALL)

    if css_matches:
        print("   ✅ PASS: CSS properly applies dimmed opacity")
    else:
        print("   ❌ FAIL: CSS dimmed class not properly configured")

    # Test 4: Performance hotspot icons (no red glow)
    print("\n4. ⚠️ PERFORMANCE HOTSPOTS")
    print("-" * 30)

    # Check NO pulse animation
    pulse_pattern = r"pulse-hotspot|hotspot-pulse"
    pulse_matches = re.findall(pulse_pattern, html_content, re.IGNORECASE)

    if not pulse_matches:
        print("   ✅ PASS: No pulsing animation found")
    else:
        print(f"   ❌ FAIL: Found {len(pulse_matches)} pulsing animation references")

    # Check warning icons are present
    warning_icon_pattern = r"performance-warning-icon"
    icon_matches = re.findall(warning_icon_pattern, html_content)

    if icon_matches:
        print(f"   ✅ PASS: Warning icons implemented ({len(icon_matches)} references)")
    else:
        print("   ❌ FAIL: Warning icons not found")

    # Check hotspot nodes only have border styling
    hotspot_pattern = r"\.node-(?:circle|rect)\.hotspot\s*\{[^}]*\}"
    hotspot_matches = re.findall(hotspot_pattern, html_content, re.DOTALL)

    animation_in_hotspot = False
    for match in hotspot_matches:
        if "animation:" in match:
            animation_in_hotspot = True
            break

    if not animation_in_hotspot:
        print("   ✅ PASS: Hotspot nodes have no animation")
    else:
        print("   ❌ FAIL: Hotspot nodes still have animation")

    # Test 5: Overall validation
    print("\n5. 🎯 OVERALL VALIDATION")
    print("-" * 30)

    # Count total issues fixed
    tests_passed = sum(
        [
            len(edge_matches) > 0,
            len(reset_matches) > 0,
            len(opacity_matches) > 0,
            len(css_matches) > 0,
            len(pulse_matches) == 0,
            len(icon_matches) > 0,
            not animation_in_hotspot,
        ]
    )

    total_tests = 7
    pass_rate = (tests_passed / total_tests) * 100

    print(f"   Tests Passed: {tests_passed}/{total_tests} ({pass_rate:.1f}%)")

    if tests_passed == total_tests:
        print("   🎉 ALL FIXES VALIDATED SUCCESSFULLY!")
    elif tests_passed >= 5:
        print("   🟡 MOST FIXES WORKING - Minor issues remain")
    else:
        print("   🔴 MAJOR ISSUES STILL PRESENT")

    print("\n" + "=" * 50)
    print("🎯 VALIDATION COMPLETE")

    return tests_passed == total_tests


if __name__ == "__main__":
    validate_all_fixes()

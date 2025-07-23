#!/usr/bin/env python3
"""
Test script to debug specific visualization issues
"""

import re


def analyze_generated_html():
    """Analyze the generated HTML to understand why fixes aren't working"""

    html_path = "graph_output/enhanced_dependency_graph.html"

    print("🔍 DEBUGGING VISUALIZATION ISSUES")
    print("=" * 50)

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check 1: Edge highlighting logic
    print("\n1. 📝 EDGE HIGHLIGHTING LOGIC")
    print("-" * 30)

    # Find the path-highlighted edge logic
    path_highlighted_pattern = r'\.classed\("path-highlighted"[^}]+\}'
    matches = re.findall(path_highlighted_pattern, content, re.DOTALL)

    for i, match in enumerate(matches):
        print(f"   Match {i+1}: {match[:100]}...")

    # Check 2: CSS dimming opacity
    print("\n2. 🎨 CSS DIMMING SETTINGS")
    print("-" * 30)

    dimmed_patterns = [
        r"--dimmed-link-opacity:\s*([^;]+);",
        r"\.link\.dimmed[^}]+opacity:\s*([^;]+);",
    ]

    for pattern in dimmed_patterns:
        matches = re.findall(pattern, content)
        if matches:
            print(f"   Found dimming setting: {matches}")

    # Check 3: Performance hotspot handling
    print("\n3. ⚠️ PERFORMANCE HOTSPOT IMPLEMENTATION")
    print("-" * 30)

    # Look for animation or pulsing
    animation_patterns = [
        r"@keyframes\s+hotspot-pulse",
        r"\.hotspot[^}]*animation[^}]*",
        r"performance-warning-icon",
    ]

    for pattern in animation_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            print(f"   Found hotspot pattern: {pattern} -> {len(matches)} matches")
        else:
            print(f"   NOT found: {pattern}")

    # Check 4: Node class management
    print("\n4. 🔵 NODE CLASS MANAGEMENT")
    print("-" * 30)

    # Look for how nodes get highlighted/unhighlighted
    class_patterns = [
        r'\.classed\("highlighted"[^}]+',
        r'\.classed\("dimmed"[^}]+',
        r'\.classed\("path-highlighted"[^}]+',
    ]

    for pattern in class_patterns:
        matches = re.findall(pattern, content)
        print(f"   {pattern}: {len(matches)} occurrences")

    # Check 5: Event handling for deselection
    print("\n5. 🖱️ EVENT HANDLING")
    print("-" * 30)

    event_patterns = [
        r"function\s+clearHighlights",
        r"function\s+resetHighlighting",
        r'\.on\("click"[^}]+clearHighlights',
    ]

    for pattern in event_patterns:
        matches = re.findall(pattern, content)
        if matches:
            print(f"   Found: {pattern} -> {len(matches)} matches")

    print("\n" + "=" * 50)
    print("🎯 ANALYSIS COMPLETE")


if __name__ == "__main__":
    analyze_generated_html()

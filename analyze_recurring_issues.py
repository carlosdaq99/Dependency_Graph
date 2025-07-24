#!/usr/bin/env python3
"""
Analyze Recurring Issues in Dependency Graph Application
========================================================

Following Multi-Stage Action Plan to identify root causes of persistent problems:
1. Blue edges between orange & blue nodes not showing
2. Edges not being dimmed according to settings
3. Performance hotspot tooltip issues
4. Horizontal tooltip positioning

This script creates a comprehensive analysis of the codebase structure.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
import ast


def analyze_project_structure():
    """Phase 1: Detailed structure analysis"""
    print("🔍 PHASE 1: COMPREHENSIVE PROJECT STRUCTURE ANALYSIS")
    print("=" * 80)

    root_path = Path(".")

    # 1. File Organization Analysis
    print("\n📁 FILE ORGANIZATION ANALYSIS:")

    # Count different file types
    file_counts = defaultdict(int)
    duplicate_patterns = defaultdict(list)

    for file_path in root_path.rglob("*.py"):
        file_counts["python"] += 1

        # Check for duplicate patterns (_new, _backup, etc.)
        stem = file_path.stem
        if stem.endswith(("_new", "_backup", "_old")):
            base_name = re.sub(r"_(new|backup|old)$", "", stem)
            duplicate_patterns[base_name].append(str(file_path))

    for file_path in root_path.rglob("*.html"):
        file_counts["html"] += 1

    for file_path in root_path.rglob("*.js"):
        file_counts["javascript"] += 1

    for file_path in root_path.rglob("*.css"):
        file_counts["css"] += 1

    print(f"   📊 Total Python files: {file_counts['python']}")
    print(f"   📊 Total HTML files: {file_counts['html']}")
    print(f"   📊 Total JS files: {file_counts['javascript']}")
    print(f"   📊 Total CSS files: {file_counts['css']}")

    # 2. Duplicate File Analysis
    print(f"\n🔄 DUPLICATE FILE PATTERNS DETECTED:")
    for base_name, files in duplicate_patterns.items():
        if len(files) > 1:
            print(f"   ⚠️ {base_name}: {len(files)} versions")
            for file in files:
                print(f"      - {file}")

    # 3. Module Structure Analysis
    print(f"\n🏗️ MODULE STRUCTURE ANALYSIS:")

    graph_modules_path = root_path / "graph_modules"
    if graph_modules_path.exists():
        print(f"   📦 graph_modules package structure:")

        for item in graph_modules_path.iterdir():
            if item.is_dir() and item.name != "__pycache__":
                print(f"      📁 {item.name}/")
                for subitem in item.iterdir():
                    if subitem.is_file() and subitem.suffix == ".py":
                        print(f"         📄 {subitem.name}")
            elif item.is_file() and item.suffix == ".py":
                print(f"      📄 {item.name}")

    return duplicate_patterns


def analyze_css_styles():
    """Phase 2: CSS style consistency analysis"""
    print("\n🎨 PHASE 2: CSS STYLE CONSISTENCY ANALYSIS")
    print("=" * 80)

    css_files = []
    style_definitions = defaultdict(list)

    # Find all CSS content (both .css files and embedded in Python)
    root_path = Path(".")

    # Check .css files
    for css_file in root_path.rglob("*.css"):
        css_files.append(css_file)

    # Check Python files for embedded CSS
    python_css_files = []
    for py_file in root_path.rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8")
            if "css" in content.lower() and any(
                selector in content
                for selector in [".node", ".link", ".tooltip", "path-highlighted"]
            ):
                python_css_files.append(py_file)
        except Exception as e:
            continue

    print(f"   📊 Found {len(css_files)} dedicated CSS files")
    print(f"   📊 Found {len(python_css_files)} Python files with CSS content")

    # Analyze key style patterns
    key_patterns = [
        r"\.node[^{]*\{[^}]*\}",
        r"\.link[^{]*\{[^}]*\}",
        r"\.tooltip[^{]*\{[^}]*\}",
        r"path-highlighted[^{]*\{[^}]*\}",
        r"dimmed[^{]*\{[^}]*\}",
        r"orange[^{]*\{[^}]*\}",
        r"blue[^{]*\{[^}]*\}",
    ]

    print(f"\n🔍 ANALYZING KEY CSS PATTERNS:")

    all_files = css_files + python_css_files
    for file_path in all_files:
        try:
            content = file_path.read_text(encoding="utf-8")
            print(f"\n   📄 {file_path}:")

            for pattern in key_patterns:
                matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
                if matches:
                    pattern_name = (
                        pattern.split("[")[0].replace("\\", "").replace(".", "")
                    )
                    print(f"      ✅ {pattern_name}: {len(matches)} definitions")
                    style_definitions[pattern_name].extend(
                        [(str(file_path), match) for match in matches]
                    )
        except Exception as e:
            print(f"      ❌ Error reading {file_path}: {e}")

    return style_definitions


def analyze_javascript_interactions():
    """Phase 3: JavaScript interaction analysis"""
    print("\n⚙️ PHASE 3: JAVASCRIPT INTERACTION ANALYSIS")
    print("=" * 80)

    js_content_files = []
    interaction_patterns = defaultdict(list)

    root_path = Path(".")

    # Find JavaScript content (both .js files and embedded in Python)
    for js_file in root_path.rglob("*.js"):
        js_content_files.append(js_file)

    for py_file in root_path.rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8")
            if any(
                js_keyword in content
                for js_keyword in [
                    "d3.",
                    "function",
                    "addEventListener",
                    "querySelector",
                ]
            ):
                js_content_files.append(py_file)
        except Exception:
            continue

    print(f"   📊 Found {len(js_content_files)} files with JavaScript content")

    # Key interaction patterns to analyze
    interaction_keywords = [
        "path-highlighted",
        "dimmed",
        "tooltip",
        "orange",
        "blue",
        "addEventListener",
        "classList.add",
        "classList.remove",
        "style.opacity",
        "d3.select",
    ]

    print(f"\n🔍 ANALYZING INTERACTION PATTERNS:")

    for file_path in js_content_files:
        try:
            content = file_path.read_text(encoding="utf-8")
            print(f"\n   📄 {file_path}:")

            for keyword in interaction_keywords:
                if keyword in content:
                    matches = content.count(keyword)
                    print(f"      ✅ {keyword}: {matches} occurrences")
                    interaction_patterns[keyword].append((str(file_path), matches))
        except Exception as e:
            print(f"      ❌ Error reading {file_path}: {e}")

    return interaction_patterns


def analyze_specific_issues():
    """Phase 4: Specific recurring issue analysis"""
    print("\n🚨 PHASE 4: SPECIFIC RECURRING ISSUE ANALYSIS")
    print("=" * 80)

    issues_found = []
    root_path = Path(".")

    # Issue 1: Blue edges between orange & blue nodes not showing
    print(f"\n🔍 ISSUE 1: Blue edges between orange & blue nodes visibility")

    edge_color_files = []
    for py_file in root_path.rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8")
            if (
                "blue" in content.lower()
                and "orange" in content.lower()
                and "edge" in content.lower()
            ):
                edge_color_files.append(py_file)
        except Exception:
            continue

    print(f"   📊 Found {len(edge_color_files)} files handling edge colors")
    for file_path in edge_color_files:
        print(f"      📄 {file_path}")

    # Issue 2: Edges not being dimmed
    print(f"\n🔍 ISSUE 2: Edge dimming functionality")

    dimming_files = []
    for file_path in root_path.rglob("*.py"):
        try:
            content = file_path.read_text(encoding="utf-8")
            if "dimmed" in content.lower() and (
                "edge" in content.lower() or "link" in content.lower()
            ):
                dimming_files.append(file_path)
        except Exception:
            continue

    print(f"   📊 Found {len(dimming_files)} files handling edge dimming")
    for file_path in dimming_files:
        print(f"      📄 {file_path}")

    # Issue 3: Tooltip positioning
    print(f"\n🔍 ISSUE 3: Tooltip horizontal positioning")

    tooltip_files = []
    for file_path in root_path.rglob("*.py"):
        try:
            content = file_path.read_text(encoding="utf-8")
            if "tooltip" in content.lower() and (
                "horizontal" in content.lower()
                or "position" in content.lower()
                or "left" in content.lower()
            ):
                tooltip_files.append(file_path)
        except Exception:
            continue

    print(f"   📊 Found {len(tooltip_files)} files handling tooltip positioning")
    for file_path in tooltip_files:
        print(f"      📄 {file_path}")

    return {
        "edge_color_files": edge_color_files,
        "dimming_files": dimming_files,
        "tooltip_files": tooltip_files,
    }


def analyze_code_duplication():
    """Phase 5: Code duplication analysis"""
    print("\n🔄 PHASE 5: CODE DUPLICATION ANALYSIS")
    print("=" * 80)

    root_path = Path(".")

    # Find potential duplicate code patterns
    similar_functions = defaultdict(list)

    for py_file in root_path.rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8")

            # Extract function definitions
            function_pattern = r"def\s+(\w+)\s*\([^)]*\):"
            functions = re.findall(function_pattern, content)

            for func_name in functions:
                similar_functions[func_name].append(str(py_file))

        except Exception:
            continue

    print(f"\n🔍 POTENTIAL DUPLICATE FUNCTIONS:")
    duplicate_count = 0

    for func_name, files in similar_functions.items():
        if len(files) > 1:
            duplicate_count += 1
            print(f"   ⚠️ {func_name}: found in {len(files)} files")
            for file_path in files:
                print(f"      - {file_path}")

    print(f"\n📊 Total potentially duplicated functions: {duplicate_count}")

    return similar_functions


def main():
    """Main analysis function following Multi-Stage Action Plan"""
    print("🚀 COMPREHENSIVE RECURRING ISSUES ANALYSIS")
    print("Following Multi-Stage Action Plan Guidelines")
    print("=" * 80)

    try:
        # Phase 1: Structure Analysis
        duplicate_patterns = analyze_project_structure()

        # Phase 2: CSS Analysis
        style_definitions = analyze_css_styles()

        # Phase 3: JavaScript Analysis
        interaction_patterns = analyze_javascript_interactions()

        # Phase 4: Specific Issues
        specific_issues = analyze_specific_issues()

        # Phase 5: Code Duplication
        duplicate_functions = analyze_code_duplication()

        # Generate summary report
        print("\n📋 SUMMARY REPORT")
        print("=" * 80)

        print(f"\n🔍 KEY FINDINGS:")
        print(f"   📦 Duplicate file patterns: {len(duplicate_patterns)}")
        print(f"   🎨 CSS style definitions: {len(style_definitions)}")
        print(f"   ⚙️ JavaScript patterns: {len(interaction_patterns)}")
        print(f"   🚨 Issue-related files: {len(specific_issues)}")
        print(
            f"   🔄 Duplicate functions: {sum(1 for funcs in duplicate_functions.values() if len(funcs) > 1)}"
        )

        print(f"\n🎯 RECOMMENDED NEXT STEPS:")
        print(f"   1. Consolidate duplicate files (especially _new variants)")
        print(f"   2. Unify CSS style definitions across modules")
        print(f"   3. Debug specific edge coloring and dimming logic")
        print(f"   4. Fix tooltip positioning calculations")
        print(f"   5. Eliminate code duplication")

        return {
            "duplicate_patterns": duplicate_patterns,
            "style_definitions": style_definitions,
            "interaction_patterns": interaction_patterns,
            "specific_issues": specific_issues,
            "duplicate_functions": duplicate_functions,
        }

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return None


if __name__ == "__main__":
    results = main()

    if results:
        print(f"\n✅ Analysis complete! Results available for next phase.")
    else:
        print(f"\n❌ Analysis failed. Check error messages above.")

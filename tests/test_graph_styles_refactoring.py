#!/usr/bin/env python3
"""
Graph Styles Module Refactoring Test
====================================

Comprehensive test suite for the refactored graph_styles module.
Tests backward compatibility, functionality, and size compliance.
"""

import sys
import os
import importlib
import traceback
from pathlib import Path

# Add the parent directory to sys.path to import graph_modules
parent_dir = Path(__file__).parent
sys.path.insert(0, str(parent_dir))


def test_file_sizes():
    """Test that all graph_styles files are under the size limit."""
    print("=== File Size Compliance Test ===")

    styles_dir = parent_dir / "graph_modules" / "graph_styles_internal"
    max_size_kb = 15
    results = []

    if styles_dir.exists():
        for file_path in styles_dir.glob("*.py"):
            size_kb = file_path.stat().st_size / 1024
            is_compliant = size_kb <= max_size_kb
            results.append((file_path.name, size_kb, is_compliant))

            status = "✅ PASS" if is_compliant else "❌ FAIL"
            print(f"{status} {file_path.name}: {size_kb:.2f} KB")

    # Check main module file
    main_file = parent_dir / "graph_modules" / "graph_styles.py"
    if main_file.exists():
        size_kb = main_file.stat().st_size / 1024
        is_compliant = size_kb <= max_size_kb
        results.append(("graph_styles.py", size_kb, is_compliant))

        status = "✅ PASS" if is_compliant else "❌ FAIL"
        print(f"{status} graph_styles.py: {size_kb:.2f} KB")

    all_compliant = all(result[2] for result in results)
    print(f"\nOverall size compliance: {'✅ PASS' if all_compliant else '❌ FAIL'}")
    return all_compliant


def test_imports():
    """Test that all modules can be imported successfully."""
    print("\n=== Import Test ===")

    test_cases = [
        ("graph_modules.graph_styles", "Main module"),
        ("graph_modules.graph_styles_internal.base_styles", "Base styles submodule"),
        (
            "graph_modules.graph_styles_internal.layout_styles",
            "Layout styles submodule",
        ),
    ]

    results = []
    for module_name, description in test_cases:
        try:
            module = importlib.import_module(module_name)
            print(f"✅ PASS: {description} ({module_name})")
            results.append(True)
        except Exception as e:
            print(f"❌ FAIL: {description} ({module_name})")
            print(f"   Error: {e}")
            results.append(False)

    all_passed = all(results)
    print(f"\nOverall import test: {'✅ PASS' if all_passed else '❌ FAIL'}")
    return all_passed


def test_backward_compatibility():
    """Test that the original API is preserved."""
    print("\n=== Backward Compatibility Test ===")

    try:
        from graph_modules.graph_styles import get_styles

        # Test main function exists and returns CSS
        css_content = get_styles()

        # Basic validation checks
        checks = [
            (isinstance(css_content, str), "Returns string"),
            (len(css_content) > 1000, "Returns substantial content"),
            (":root" in css_content, "Contains CSS variables"),
            (".node-rect" in css_content, "Contains node styles"),
            (".controls" in css_content, "Contains control styles"),
            ("@media" in css_content, "Contains responsive styles"),
            ("[data-theme=" in css_content, "Contains theme support"),
        ]

        results = []
        for check, description in checks:
            status = "✅ PASS" if check else "❌ FAIL"
            print(f"{status} {description}")
            results.append(check)

        # Test legacy function if it exists
        try:
            from graph_modules.graph_styles import get_css_styles

            legacy_css = get_css_styles()
            legacy_match = css_content == legacy_css
            status = "✅ PASS" if legacy_match else "❌ FAIL"
            print(f"{status} Legacy function compatibility")
            results.append(legacy_match)
        except ImportError:
            print("⚠️  WARN: Legacy function get_css_styles not found")

        all_passed = all(results)
        print(
            f"\nOverall backward compatibility: {'✅ PASS' if all_passed else '❌ FAIL'}"
        )
        return all_passed

    except Exception as e:
        print(f"❌ FAIL: Could not test backward compatibility")
        print(f"   Error: {e}")
        traceback.print_exc()
        return False


def test_submodule_functionality():
    """Test that individual submodules work correctly."""
    print("\n=== Submodule Functionality Test ===")

    results = []

    # Test base_styles module
    try:
        from graph_modules.graph_styles_internal.base_styles import get_base_styles_css

        base_css = get_base_styles_css()

        base_checks = [
            (isinstance(base_css, str), "Base styles returns string"),
            (":root" in base_css, "Base styles contains variables"),
            ("[data-theme=" in base_css, "Base styles contains theme support"),
            ("body" in base_css, "Base styles contains body styling"),
        ]

        for check, description in base_checks:
            status = "✅ PASS" if check else "❌ FAIL"
            print(f"{status} {description}")
            results.append(check)

    except Exception as e:
        print(f"❌ FAIL: Base styles module error: {e}")
        results.append(False)

    # Test layout_styles module
    try:
        from graph_modules.graph_styles_internal.layout_styles import (
            get_layout_styles_css,
        )

        layout_css = get_layout_styles_css()

        layout_checks = [
            (isinstance(layout_css, str), "Layout styles returns string"),
            (".node-rect" in layout_css, "Layout styles contains node styles"),
            (".link" in layout_css, "Layout styles contains link styles"),
            ("@media" in layout_css, "Layout styles contains responsive design"),
        ]

        for check, description in layout_checks:
            status = "✅ PASS" if check else "❌ FAIL"
            print(f"{status} {description}")
            results.append(check)

    except Exception as e:
        print(f"❌ FAIL: Layout styles module error: {e}")
        results.append(False)

    all_passed = all(results)
    print(
        f"\nOverall submodule functionality: {'✅ PASS' if all_passed else '❌ FAIL'}"
    )
    return all_passed


def test_css_content_coverage():
    """Test that the combined CSS contains all expected features."""
    print("\n=== CSS Content Coverage Test ===")

    try:
        from graph_modules.graph_styles import get_styles

        css_content = get_styles()

        # Expected CSS features
        expected_features = [
            # Theme support
            ":root",
            '[data-theme="dark"]',
            "--bg-primary",
            "--text-primary",
            # Base elements
            "body",
            ".container",
            ".controls",
            ".graph-container",
            # Node styling
            ".node-rect",
            ".node-circle",
            ".node-label",
            # Link styling
            ".link",
            ".link.highlighted",
            ".link.dimmed",
            # Interactive elements
            ".folder-item",
            ".toggle-switch",
            ".theme-toggle",
            # Responsive design
            "@media (max-width: 768px)",
            # Accessibility
            ":focus",
            "@media (prefers-reduced-motion",
            # Animations
            "@keyframes",
            "transition:",
        ]

        results = []
        for feature in expected_features:
            present = feature in css_content
            status = "✅ PASS" if present else "❌ FAIL"
            print(f"{status} {feature}")
            results.append(present)

        coverage_percent = (sum(results) / len(results)) * 100
        print(f"\nCSS Feature Coverage: {coverage_percent:.1f}%")

        all_passed = coverage_percent >= 90  # 90% coverage threshold
        print(f"Overall CSS coverage: {'✅ PASS' if all_passed else '❌ FAIL'}")
        return all_passed

    except Exception as e:
        print(f"❌ FAIL: Could not test CSS content coverage")
        print(f"   Error: {e}")
        return False


def run_all_tests():
    """Run all tests and provide summary."""
    print("Graph Styles Module Refactoring Test Suite")
    print("=" * 50)

    test_functions = [
        test_file_sizes,
        test_imports,
        test_backward_compatibility,
        test_submodule_functionality,
        test_css_content_coverage,
    ]

    results = []
    for test_func in test_functions:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ FAIL: {test_func.__name__} encountered an error")
            print(f"   Error: {e}")
            traceback.print_exc()
            results.append(False)

    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)

    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100

    for i, (test_func, result) in enumerate(zip(test_functions, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_func.__name__}")

    print(f"\nOverall Success Rate: {success_rate:.1f}% ({passed}/{total})")

    if success_rate == 100:
        print("🎉 All tests passed! Graph styles refactoring successful.")
        return True
    else:
        print("⚠️  Some tests failed. Review the results above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

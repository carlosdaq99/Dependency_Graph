#!/usr/bin/env python3
"""
Quick Test Script for Import and Syntax Validation
=================================================

This script provides a fast way to test imports and basic syntax
before running the comprehensive test suite.
"""

import sys
import os
import importlib

# Add workspace to path
sys.path.insert(0, os.path.abspath("."))


def test_basic_imports():
    """Test basic imports of all main modules."""
    print("🧪 Testing Basic Imports...")
    print("-" * 40)

    modules_to_test = [
        "graph_modules",
        "graph_modules.dependency_analyzer",
        "graph_modules.graph_styles",
        "graph_modules.graph_controls",
        "graph_modules.graph_visualization",
        "graph_modules.html_generator",
        "graph_modules.force_directed_layout",
        "graph_modules.git_analysis",
        "graph_modules.hierarchical_layout",
    ]

    success_count = 0
    total_count = len(modules_to_test)

    for module_name in modules_to_test:
        try:
            importlib.import_module(module_name)
            print(f"  ✅ {module_name}: Success")
            success_count += 1
        except ImportError as e:
            print(f"  ❌ {module_name}: ImportError - {e}")
        except Exception as e:
            print(f"  ❌ {module_name}: Error - {e}")

    print("-" * 40)
    print(
        f"📊 Import Results: {success_count}/{total_count} modules imported successfully"
    )

    return success_count == total_count


def test_key_functions():
    """Test that key functions are available and callable."""
    print("\n🔧 Testing Key Functions...")
    print("-" * 40)

    success = True

    try:
        from graph_modules.dependency_analyzer import EnhancedDependencyAnalyzer

        EnhancedDependencyAnalyzer()
        print("  ✅ EnhancedDependencyAnalyzer: Created successfully")
    except Exception as e:
        print(f"  ❌ EnhancedDependencyAnalyzer: {e}")
        success = False

    try:
        from graph_modules.graph_styles import get_styles

        styles = get_styles()
        if styles and len(styles) > 100:
            print("  ✅ get_styles: Returns valid CSS")
        else:
            print("  ❌ get_styles: Returns invalid content")
            success = False
    except Exception as e:
        print(f"  ❌ get_styles: {e}")
        success = False

    try:
        from graph_modules.graph_controls import get_graph_controls_js

        controls = get_graph_controls_js()
        if controls and len(controls) > 100:
            print("  ✅ get_graph_controls_js: Returns valid JS")
        else:
            print("  ❌ get_graph_controls_js: Returns invalid content")
            success = False
    except Exception as e:
        print(f"  ❌ get_graph_controls_js: {e}")
        success = False

    try:
        from graph_modules.graph_visualization import get_graph_visualization_js

        viz = get_graph_visualization_js()
        if viz and len(viz) > 100:
            print("  ✅ get_graph_visualization_js: Returns valid JS")
        else:
            print("  ❌ get_graph_visualization_js: Returns invalid content")
            success = False
    except Exception as e:
        print(f"  ❌ get_graph_visualization_js: {e}")
        success = False

    return success


def main():
    """Run quick import and syntax tests."""
    print("🚀 Quick Import and Syntax Test")
    print("=" * 50)

    imports_ok = test_basic_imports()
    functions_ok = test_key_functions()

    print("\n" + "=" * 50)
    if imports_ok and functions_ok:
        print("✅ ALL TESTS PASSED - Ready for comprehensive testing!")
        return 0
    else:
        print("❌ TESTS FAILED - Fix issues before comprehensive testing")
        if not imports_ok:
            print("   • Import issues detected")
        if not functions_ok:
            print("   • Function issues detected")
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Test the refactored graph_visualization module.
Verify that the split modules work correctly and maintain the original API.
"""

import sys


def test_graph_visualization_refactor():
    """Test that the refactored graph_visualization module works correctly."""
    print("🧪 Testing refactored graph_visualization module...")

    try:
        # Test importing the main module
        from graph_modules.graph_visualization import get_graph_visualization_js

        print("  ✅ Main module import: SUCCESS")

        # Test that the function returns a string
        js_code = get_graph_visualization_js()
        if isinstance(js_code, str) and len(js_code) > 1000:
            print(
                f"  ✅ Function returns JavaScript string: SUCCESS ({len(js_code)} chars)"
            )
        else:
            print(
                f"  ❌ Function return issue: Expected large string, got {type(js_code)} with length {len(js_code) if hasattr(js_code, '__len__') else 'N/A'}"
            )
            return False

        # Test that all expected functions are present in the JavaScript
        expected_functions = [
            "initializeEnhancedVisualization",
            "initializeHierarchicalLayout",
            "initializeForceDirectedLayout",
            "handleEnhancedNodeClick",
            "switchToLayout",
            "calculateCircleRadius",
            "addNodeLabels",
            "updateEnhancedVisibility",
        ]

        missing_functions = []
        for func in expected_functions:
            if func not in js_code:
                missing_functions.append(func)

        if missing_functions:
            print(f"  ❌ Missing functions: {missing_functions}")
            return False
        else:
            print(
                f"  ✅ All expected functions present: SUCCESS ({len(expected_functions)} functions)"
            )

        # Test individual submodules
        from graph_modules.graph_visualization.core import get_core_visualization_js
        from graph_modules.graph_visualization.layouts import (
            get_layouts_visualization_js,
        )
        from graph_modules.graph_visualization.interactions import (
            get_interactions_visualization_js,
        )
        from graph_modules.graph_visualization.rendering import (
            get_rendering_visualization_js,
        )

        print("  ✅ All submodules import successfully: SUCCESS")

        # Test that submodules return non-empty strings
        submodule_results = {
            "core": get_core_visualization_js(),
            "layouts": get_layouts_visualization_js(),
            "interactions": get_interactions_visualization_js(),
            "rendering": get_rendering_visualization_js(),
        }

        for name, result in submodule_results.items():
            if isinstance(result, str) and len(result) > 100:
                print(
                    f"  ✅ {name} submodule returns valid JS: SUCCESS ({len(result)} chars)"
                )
            else:
                print(
                    f"  ❌ {name} submodule issue: Expected string, got {type(result)}"
                )
                return False

        # Test that combined length matches
        combined_length = sum(len(result) for result in submodule_results.values())
        # Allow for some difference due to newlines added in combination
        if abs(len(js_code) - combined_length) <= 10:
            print(
                f"  ✅ Combined length matches: SUCCESS (main: {len(js_code)}, combined: {combined_length})"
            )
        else:
            print(
                f"  ⚠️ Length difference: main={len(js_code)}, combined={combined_length}, diff={abs(len(js_code) - combined_length)}"
            )

        return True

    except Exception as e:
        print(f"  ❌ Test failed with exception: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("🚀 Starting graph_visualization refactor tests...")
    print("=" * 60)

    success = test_graph_visualization_refactor()

    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! Refactoring successful.")
        return 0
    else:
        print("❌ Tests failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

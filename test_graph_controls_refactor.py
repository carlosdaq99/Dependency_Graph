#!/usr/bin/env python3
"""
Test the refactored graph_controls module.
Verify that the split modules work correctly and maintain the original API.
"""

import sys


def test_graph_controls_refactor():
    """Test that the refactored graph_controls module works correctly."""
    print("🧪 Testing refactored graph_controls module...")

    try:
        # Test importing the main module
        from graph_modules.graph_controls import get_graph_controls_js

        print("  ✅ Main module import: SUCCESS")

        # Test that the function returns a string
        js_code = get_graph_controls_js()
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
            "initializeTheme",
            "toggleTheme",
            "updateEnhancedControls",
            "updateEnhancedStats",
            "toggleFolder",
            "toggleTestDependencies",
            "setupAdvancedFilters",
            "setupLayoutToggle",
            "initializeControls",
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
        from graph_modules.graph_controls.ui_controls import get_ui_controls_js
        from graph_modules.graph_controls.event_handlers import get_event_handlers_js

        print("  ✅ All submodules import successfully: SUCCESS")

        # Test that submodules return non-empty strings
        submodule_results = {
            "ui_controls": get_ui_controls_js(),
            "event_handlers": get_event_handlers_js(),
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
    print("🚀 Starting graph_controls refactor tests...")
    print("=" * 60)

    success = test_graph_controls_refactor()

    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! Refactoring successful.")
        return 0
    else:
        print("❌ Tests failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

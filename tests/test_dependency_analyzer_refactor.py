#!/usr/bin/env python3
"""
Test the refactored dependency_analyzer module.
Verify that the split modules work correctly and maintain the original API.
"""

import sys


def test_dependency_analyzer_refactor():
    """Test that the refactored dependency_analyzer module works correctly."""
    print("🧪 Testing refactored dependency_analyzer module...")

    try:
        # Test importing the main class
        from graph_modules.dependency_analyzer import EnhancedDependencyAnalyzer

        print("  ✅ Main class import: SUCCESS")

        # Test instantiation
        analyzer = EnhancedDependencyAnalyzer()
        print("  ✅ Class instantiation: SUCCESS")

        # Test that key attributes exist
        expected_attributes = [
            "dependencies",
            "node_importance",
            "exclude_folders",
            "import_resolver",
            "performance_analyzer",
            "importance_calculator",
        ]

        missing_attributes = []
        for attr in expected_attributes:
            if not hasattr(analyzer, attr):
                missing_attributes.append(attr)

        if missing_attributes:
            print(f"  ❌ Missing attributes: {missing_attributes}")
            return False
        else:
            print(
                f"  ✅ All expected attributes present: SUCCESS ({len(expected_attributes)} attributes)"
            )

        # Test that key methods exist
        expected_methods = [
            "analyze_project",
            "create_unique_id",
            "get_folder_name",
            "is_test_file",
        ]

        missing_methods = []
        for method in expected_methods:
            if not hasattr(analyzer, method) or not callable(getattr(analyzer, method)):
                missing_methods.append(method)

        if missing_methods:
            print(f"  ❌ Missing methods: {missing_methods}")
            return False
        else:
            print(
                f"  ✅ All expected methods present: SUCCESS ({len(expected_methods)} methods)"
            )

        # Test individual submodules
        from graph_modules.dependency_analyzer.core import (
            EnhancedDependencyAnalyzer as CoreAnalyzer,
        )
        from graph_modules.dependency_analyzer.import_resolver import ImportResolver
        from graph_modules.dependency_analyzer.metrics import (
            PerformanceAnalyzer,
            ImportanceCalculator,
        )

        print("  ✅ All submodules import successfully: SUCCESS")

        # Test that helper classes can be instantiated
        test_analyzer = CoreAnalyzer()
        import_resolver = ImportResolver(test_analyzer)
        performance_analyzer = PerformanceAnalyzer(test_analyzer)
        importance_calculator = ImportanceCalculator(test_analyzer)

        print("  ✅ All helper classes instantiate: SUCCESS")

        # Test that the analyzer has the helper instances
        if (
            hasattr(analyzer, "import_resolver")
            and hasattr(analyzer, "performance_analyzer")
            and hasattr(analyzer, "importance_calculator")
        ):
            print("  ✅ Helper instances attached to main analyzer: SUCCESS")
        else:
            print("  ❌ Helper instances not properly attached")
            return False

        return True

    except Exception as e:
        print(f"  ❌ Test failed with exception: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("🚀 Starting dependency_analyzer refactor tests...")
    print("=" * 60)

    success = test_dependency_analyzer_refactor()

    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! Refactoring successful.")
        return 0
    else:
        print("❌ Tests failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

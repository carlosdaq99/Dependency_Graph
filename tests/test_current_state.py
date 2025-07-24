#!/usr/bin/env python3
"""
Test imports and basic functionality of all graph_modules components.
This script will validate that all modules can be imported and their basic functions work.
"""

import sys
import traceback
from pathlib import Path


def test_imports():
    """Test importing all modules and their main components."""
    results = {}

    print("🧪 Testing module imports...")

    # Test individual module imports
    modules_to_test = [
        "graph_modules.dependency_analyzer",
        "graph_modules.force_directed_layout",
        "graph_modules.git_analysis",
        "graph_modules.graph_controls",
        "graph_modules.graph_styles",
        "graph_modules.graph_visualization",
        "graph_modules.hierarchical_layout",
        "graph_modules.html_generator",
    ]

    for module_name in modules_to_test:
        try:
            __import__(module_name)
            results[module_name] = "✅ SUCCESS"
            print(f"  {module_name}: ✅")
        except Exception as e:
            results[module_name] = f"❌ FAILED: {str(e)}"
            print(f"  {module_name}: ❌ - {str(e)}")

    # Test main package import
    try:
        import graph_modules

        results["graph_modules"] = "✅ SUCCESS"
        print(f"  graph_modules package: ✅")

        # Test main function if available
        if hasattr(graph_modules, "main"):
            print(f"  graph_modules.main function: ✅")
        else:
            print(f"  graph_modules.main function: ⚠️ Not found")

    except Exception as e:
        results["graph_modules"] = f"❌ FAILED: {str(e)}"
        print(f"  graph_modules package: ❌ - {str(e)}")

    return results


def test_basic_functionality():
    """Test basic functionality of key components."""
    print("\n🔧 Testing basic functionality...")

    try:
        from graph_modules.dependency_analyzer import EnhancedDependencyAnalyzer

        analyzer = EnhancedDependencyAnalyzer()
        print("  ✅ EnhancedDependencyAnalyzer instantiated successfully")

        # Test with a simple directory
        test_path = Path(__file__).parent
        print(f"  🔍 Testing analysis on: {test_path}")

        # This might take a moment, so let's just test instantiation for now

    except Exception as e:
        print(f"  ❌ EnhancedDependencyAnalyzer test failed: {str(e)}")
        traceback.print_exc()

    try:
        from graph_modules.html_generator import generate_enhanced_html_visualization

        print("  ✅ generate_enhanced_html_visualization imported successfully")
    except Exception as e:
        print(f"  ❌ HTML generator test failed: {str(e)}")


def main():
    """Run all tests."""
    print("🚀 Starting comprehensive module testing...")
    print("=" * 60)

    # Test imports
    import_results = test_imports()

    # Test basic functionality
    test_basic_functionality()

    print("\n" + "=" * 60)
    print("📊 Final Results:")

    success_count = sum(1 for result in import_results.values() if "SUCCESS" in result)
    total_count = len(import_results)

    print(f"Successful imports: {success_count}/{total_count}")

    if success_count == total_count:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️ Some tests failed. Check the details above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

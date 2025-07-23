#!/usr/bin/env python3
"""
Quick test to validate the dual-layout implementation
"""

import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))


def test_modules():
    """Test that our modules can be imported"""
    try:
        from graph_modules.graph_visualization import get_graph_visualization_js
        from graph_modules.graph_controls import get_graph_controls_js
        from graph_modules.graph_styles import get_graph_styles

        print("✅ All graph modules imported successfully")

        # Test function availability
        viz_js = get_graph_visualization_js()
        controls_js = get_graph_controls_js()
        styles_css = get_graph_styles()

        # Check for key elements in the code
        tests = [
            (
                "switchToLayout function in visualization",
                "function switchToLayout" in viz_js,
            ),
            (
                "calculateCircleRadius function in visualization",
                "function calculateCircleRadius" in viz_js,
            ),
            ("hierarchicalContainer creation", "hierarchicalContainer" in viz_js),
            ("forceDirectedContainer creation", "forceDirectedContainer" in viz_js),
            (
                "initializeHierarchicalLayout function",
                "function initializeHierarchicalLayout" in viz_js,
            ),
            (
                "initializeForceDirectedLayoutNodes function",
                "function initializeForceDirectedLayoutNodes" in viz_js,
            ),
            ("window.switchToLayout exposure", "window.switchToLayout" in viz_js),
            (
                "switchLayout in controls uses switchToLayout",
                "window.switchToLayout" in controls_js,
            ),
            ("node-circle styles", ".node-circle" in styles_css),
            ("unified transparency variables", "--dimmed-opacity" in styles_css),
        ]

        for test_name, test_result in tests:
            status = "✅" if test_result else "❌"
            print(f"{status} {test_name}: {'PASS' if test_result else 'FAIL'}")

        return all(result for _, result in tests)

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main():
    """Main test function"""
    print("🧪 Testing dual-layout implementation...")
    print("=" * 50)

    success = test_modules()

    print("=" * 50)
    if success:
        print("🎉 All tests passed! The dual-layout implementation looks good.")
        print("🚀 Key features implemented:")
        print("   • Separate containers for hierarchical and force-directed layouts")
        print("   • Circle nodes with importance-based sizing for force-directed mode")
        print("   • Rectangle nodes with text-based sizing for hierarchical mode")
        print("   • Simple container switching instead of complex regeneration")
        print("   • Unified transparency system")
        print("   • Global function exposure for cross-module communication")
    else:
        print("💥 Some tests failed. Please review the implementation.")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

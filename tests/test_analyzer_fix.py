#!/usr/bin/env python3
"""
Test Dependency Analyzer Fix
============================

Quick test to verify the dependency analyzer can now find Python files.
"""

import sys
import os

# Add workspace to path
sys.path.insert(0, os.path.abspath("."))


def test_dependency_analyzer():
    """Test that the dependency analyzer can find files now."""
    print("🧪 Testing Fixed Dependency Analyzer")
    print("=" * 50)

    try:
        from graph_modules.dependency_analyzer import EnhancedDependencyAnalyzer

        analyzer = EnhancedDependencyAnalyzer()
        print("✅ Analyzer created successfully")

        # Test with graph_modules directory
        test_dir = "graph_modules"
        print(f"🔍 Testing analysis of: {test_dir}")

        result = analyzer.analyze_project(test_dir)

        if result and isinstance(result, dict):
            nodes = result.get("nodes", [])
            links = result.get("links", [])

            print("✅ Analysis successful!")
            print(f"   📊 Found {len(nodes)} nodes")
            print(f"   🔗 Found {len(links)} links")

            # Show first few nodes
            if nodes:
                print("   📋 Sample nodes:")
                for node in nodes[:5]:
                    print(f"      - {node.get('id', 'Unknown')}")
                if len(nodes) > 5:
                    print(f"      ... and {len(nodes) - 5} more")

            return True
        else:
            print("❌ Analysis failed - invalid result")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run the test."""
    success = test_dependency_analyzer()

    print("\n" + "=" * 50)
    if success:
        print("🎉 DEPENDENCY ANALYZER FIX SUCCESSFUL!")
        return 0
    else:
        print("❌ DEPENDENCY ANALYZER STILL HAS ISSUES")
        return 1


if __name__ == "__main__":
    sys.exit(main())

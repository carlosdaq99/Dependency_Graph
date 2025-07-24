#!/usr/bin/env python3
"""
File Discovery Diagnostic Script
===============================

This script tests the file discovery logic to understand why the dependency analyzer
is not finding Python files in the graph_modules directory.
"""

from pathlib import Path


def test_file_discovery():
    """Test file discovery in various directories."""
    print("🔍 File Discovery Diagnostic")
    print("=" * 50)

    # Test different root paths
    test_paths = [
        ".",
        "graph_modules",
        str(Path("graph_modules").resolve()),
        str(Path(".").resolve()),
    ]

    for test_path in test_paths:
        print(f"\n📂 Testing path: {test_path}")

        root = Path(test_path)
        print(f"   Resolved to: {root.resolve()}")
        print(f"   Exists: {root.exists()}")
        print(f"   Is directory: {root.is_dir()}")

        if not root.exists():
            print("   ❌ Path does not exist")
            continue

        if not root.is_dir():
            print("   ❌ Path is not a directory")
            continue

        # List immediate contents
        try:
            contents = list(root.iterdir())
            print(f"   📋 Contains {len(contents)} items:")
            for item in contents[:10]:  # Show first 10
                item_type = "dir" if item.is_dir() else "file"
                print(f"      {item.name} ({item_type})")
            if len(contents) > 10:
                print(f"      ... and {len(contents) - 10} more")

        except PermissionError:
            print("   ❌ Permission denied")
            continue

        # Find Python files using rglob
        try:
            python_files = list(root.rglob("*.py"))
            print(f"   🐍 Found {len(python_files)} Python files:")

            for py_file in python_files[:10]:  # Show first 10
                try:
                    rel_path = py_file.relative_to(root)
                    print(f"      {rel_path}")
                except ValueError:
                    print(f"      {py_file} (outside root)")

            if len(python_files) > 10:
                print(f"      ... and {len(python_files) - 10} more")

        except Exception as e:
            print(f"   ❌ Error finding Python files: {e}")


def test_exclusion_logic():
    """Test the exclusion logic used by the analyzer."""
    print("\n🚫 Testing Exclusion Logic")
    print("=" * 50)

    # Test exclusion patterns
    exclude_folders = ["__pycache__", "dependency_graph"]

    test_files = [
        Path("graph_modules/__init__.py"),
        Path("graph_modules/dependency_analyzer/__init__.py"),
        Path("graph_modules/__pycache__/test.py"),
        Path("dependency_graph/test.py"),
        Path("some_folder/test.py"),
    ]

    for test_file in test_files:
        excluded = any(excluded in test_file.parts for excluded in exclude_folders)
        status = "❌ EXCLUDED" if excluded else "✅ INCLUDED"
        print(f"   {status} {test_file}")


def test_current_working_directory():
    """Test current working directory and paths."""
    print("\n📍 Current Working Directory Info")
    print("=" * 50)

    cwd = Path.cwd()
    print(f"   Current working directory: {cwd}")
    print(f"   Directory name: {cwd.name}")

    # Check if we're in the right place
    if "dependency_graph" in str(cwd):
        print("   ✅ Working in dependency_graph project")
    else:
        print("   ⚠️ Not in dependency_graph project directory")

    # Check for key directories
    key_dirs = ["graph_modules", "tests", "graph_output"]
    for key_dir in key_dirs:
        dir_path = cwd / key_dir
        exists = dir_path.exists()
        status = "✅" if exists else "❌"
        print(f"   {status} {key_dir}: {exists}")


def main():
    """Run all diagnostic tests."""
    test_current_working_directory()
    test_file_discovery()
    test_exclusion_logic()

    print("\n" + "=" * 50)
    print("🎯 Diagnosis complete!")


if __name__ == "__main__":
    main()

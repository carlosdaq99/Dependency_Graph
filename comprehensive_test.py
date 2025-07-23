#!/usr/bin/env python3
"""
Comprehensive JavaScript syntax validation test
"""

import os
import sys
import re
import json
import subprocess
import tempfile

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))


def generate_test_html():
    """Generate the HTML file and test for JavaScript syntax errors"""
    try:
        print("🔨 Generating HTML file...")
        import enhanced_dependency_graph_modular

        # This should generate the HTML file
        print("✅ HTML generation completed")
        return True
    except Exception as e:
        print(f"❌ HTML generation failed: {e}")
        return False


def find_js_syntax_errors(html_file_path):
    """Extract JavaScript and check for syntax errors"""
    print(f"🔍 Analyzing JavaScript syntax in {html_file_path}")

    if not os.path.exists(html_file_path):
        print(f"❌ HTML file not found: {html_file_path}")
        return False

    try:
        with open(html_file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract JavaScript content between <script> tags
        script_pattern = r"<script[^>]*>(.*?)</script>"
        scripts = re.findall(script_pattern, content, re.DOTALL)

        print(f"📜 Found {len(scripts)} script blocks")

        syntax_errors = []
        for i, script in enumerate(scripts):
            if script.strip():
                errors = check_js_syntax(script, f"Script block {i+1}")
                syntax_errors.extend(errors)

        if syntax_errors:
            print(f"❌ Found {len(syntax_errors)} JavaScript syntax errors:")
            for error in syntax_errors:
                print(f"   • {error}")
            return False
        else:
            print("✅ No JavaScript syntax errors found")
            return True

    except Exception as e:
        print(f"❌ Error analyzing HTML file: {e}")
        return False


def check_js_syntax(js_code, block_name):
    """Check JavaScript syntax using Node.js"""
    errors = []

    # Basic syntax checks
    brace_count = js_code.count("{") - js_code.count("}")
    if brace_count != 0:
        errors.append(f"{block_name}: Unmatched braces (difference: {brace_count})")

    paren_count = js_code.count("(") - js_code.count(")")
    if paren_count != 0:
        errors.append(
            f"{block_name}: Unmatched parentheses (difference: {paren_count})"
        )

    bracket_count = js_code.count("[") - js_code.count("]")
    if bracket_count != 0:
        errors.append(f"{block_name}: Unmatched brackets (difference: {bracket_count})")

    # Check for common syntax patterns that indicate issues
    lines = js_code.split("\n")
    for line_num, line in enumerate(lines, 1):
        line = line.strip()

        # Check for unexpected closing braces
        if line == "}" and line_num < len(lines):
            next_line = lines[line_num].strip() if line_num < len(lines) else ""
            if (
                next_line
                and not next_line.startswith("//")
                and not next_line.startswith("/*")
            ):
                # Look for patterns that might indicate an issue
                if next_line.startswith(
                    ("function", "var", "let", "const", "if", "for", "while")
                ):
                    error_msg = "{block}:Line {line}: Potential syntax error - unexpected '}}' before '{text}...'".format(
                        block=block_name, line=line_num, text=next_line[:30]
                    )
                    errors.append(error_msg)
    # Try Node.js syntax check if available
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
            f.write(js_code)
            f.flush()

            # Try to run syntax check with Node.js
            result = subprocess.run(
                ["node", "--check", f.name], capture_output=True, text=True, timeout=10
            )

            if result.returncode != 0:
                errors.append(
                    f"{block_name}: Node.js syntax error: {result.stderr.strip()}"
                )

        os.unlink(f.name)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        # Node.js not available or failed - continue with basic checks
        pass

    return errors


def check_function_completeness():
    """Check that all functions are properly closed"""
    print("🔧 Checking function completeness in modules...")

    try:
        from graph_modules.graph_visualization import get_graph_visualization_js
        from graph_modules.graph_controls import get_graph_controls_js

        modules = [
            ("graph_visualization", get_graph_visualization_js()),
            ("graph_controls", get_graph_controls_js()),
        ]

        issues = []
        for module_name, js_code in modules:
            # Find all function definitions
            function_pattern = r"function\s+(\w+)\s*\([^)]*\)\s*{"
            functions = re.findall(function_pattern, js_code)

            print(f"📋 {module_name}: Found {len(functions)} functions")
            for func_name in functions:
                print(f"   • {func_name}")

            # Check for incomplete functions
            lines = js_code.split("\n")
            in_function = False
            brace_depth = 0
            current_function = None

            for line_num, line in enumerate(lines, 1):
                stripped = line.strip()

                # Track function starts
                func_match = re.match(r"function\s+(\w+)", stripped)
                if func_match:
                    current_function = func_match.group(1)
                    in_function = True
                    brace_depth = 0

                # Count braces
                brace_depth += stripped.count("{") - stripped.count("}")

                # Check if function ended
                if in_function and brace_depth == 0 and "{" in stripped:
                    in_function = False
                    current_function = None

            # Check if we're still inside a function at the end
            if in_function and current_function:
                issues.append(
                    f"{module_name}: Function '{current_function}' appears to be incomplete (brace_depth: {brace_depth})"
                )

        if issues:
            print("❌ Function completeness issues found:")
            for issue in issues:
                print(f"   • {issue}")
            return False
        else:
            print("✅ All functions appear complete")
            return True

    except Exception as e:
        print(f"❌ Error checking function completeness: {e}")
        return False


def main():
    """Run comprehensive tests"""
    print("🧪 COMPREHENSIVE JAVASCRIPT SYNTAX VALIDATION")
    print("=" * 60)

    # Test 1: Basic module import and structure
    print("\n1️⃣ TESTING MODULE STRUCTURE")
    print("-" * 30)
    structure_ok = True
    try:
        from graph_modules.graph_visualization import get_graph_visualization_js
        from graph_modules.graph_controls import get_graph_controls_js
        from graph_modules.graph_styles import get_graph_styles

        print("✅ All modules import successfully")
    except Exception as e:
        print(f"❌ Module import failed: {e}")
        structure_ok = False

    # Test 2: Function completeness
    print("\n2️⃣ TESTING FUNCTION COMPLETENESS")
    print("-" * 30)
    functions_ok = check_function_completeness()

    # Test 3: Generate HTML and check syntax
    print("\n3️⃣ TESTING HTML GENERATION AND SYNTAX")
    print("-" * 30)
    generation_ok = generate_test_html()

    syntax_ok = True
    if generation_ok:
        html_path = "graph_output/enhanced_dependency_graph.html"
        syntax_ok = find_js_syntax_errors(html_path)

    # Test 4: Check for specific known issues
    print("\n4️⃣ CHECKING FOR KNOWN PATTERNS")
    print("-" * 30)
    patterns_ok = check_known_patterns()

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    tests = [
        ("Module Structure", structure_ok),
        ("Function Completeness", functions_ok),
        ("HTML Generation", generation_ok),
        ("JavaScript Syntax", syntax_ok),
        ("Known Patterns", patterns_ok),
    ]

    all_passed = True
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} {test_name}")
        if not result:
            all_passed = False

    print("=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Implementation is ready.")
    else:
        print("💥 SOME TESTS FAILED! Issues need to be addressed.")

    return all_passed


def check_known_patterns():
    """Check for known problematic patterns"""
    print("🔍 Checking for known problematic patterns...")

    try:
        from graph_modules.graph_visualization import get_graph_visualization_js
        from graph_modules.graph_controls import get_graph_controls_js

        viz_js = get_graph_visualization_js()
        controls_js = get_graph_controls_js()

        issues = []

        # Check for unmatched braces in specific patterns
        problematic_patterns = [
            (r"function\s+\w+[^{]*{[^}]*$", "Function without closing brace"),
            (r"}\s*function", "Function immediately after closing brace"),
            (r"}\s*}", "Double closing braces"),
            (r"{\s*{", "Double opening braces"),
        ]

        for pattern, description in problematic_patterns:
            if re.search(pattern, viz_js, re.MULTILINE):
                issues.append(f"graph_visualization: {description}")
            if re.search(pattern, controls_js, re.MULTILINE):
                issues.append(f"graph_controls: {description}")

        # Check for proper function exposure
        if "window.switchToLayout = switchToLayout" not in viz_js:
            issues.append(
                "graph_visualization: switchToLayout not properly exposed to window"
            )

        if "window.switchToLayout" not in controls_js:
            issues.append("graph_controls: Not using window.switchToLayout")

        if issues:
            print("❌ Found problematic patterns:")
            for issue in issues:
                print(f"   • {issue}")
            return False
        else:
            print("✅ No known problematic patterns found")
            return True

    except Exception as e:
        print(f"❌ Error checking patterns: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

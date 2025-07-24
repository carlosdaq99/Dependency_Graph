#!/usr/bin/env python3
"""Debug the HTML generation to see what's happening."""

import sys
from pathlib import Path

# Add the graph_modules directory to the path
sys.path.insert(0, str(Path(__file__).parent))


def debug_html_generation():
    """Debug HTML generation."""
    from graph_modules.html_generator import generate_enhanced_html_visualization

    # Create mock graph data
    mock_data = {
        "nodes": [
            {
                "id": "test_file.py",
                "name": "test_file",
                "folder": "root",
                "size": 5120,
                "total_lines": 120,
                "performance_score": 0.75,
                "is_test": False,
            }
        ],
        "edges": [],
        "subfolder_info": {"root": {"count": 1}},
    }

    try:
        html_content = generate_enhanced_html_visualization(mock_data)

        print("HTML Content Type:", type(html_content))
        print("HTML Content Length:", len(str(html_content)))

        # Check if it's a string
        if isinstance(html_content, str):
            print("✅ HTML is a string")
            print("First 500 chars:")
            print(html_content[:500])
            print("\n...")
            print("Last 500 chars:")
            print(html_content[-500:])

            # Check for our key items
            if "Layout Controls" in html_content:
                print("✅ Contains 'Layout Controls'")
            else:
                print("❌ Missing 'Layout Controls'")

            if "Average SLOC" in html_content:
                print("✅ Contains 'Average SLOC'")
            else:
                print("❌ Missing 'Average SLOC'")
        else:
            print("❌ HTML is not a string, it's:", type(html_content))
            print("Value:", repr(html_content))

    except Exception as e:
        print("❌ Error:", e)
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    debug_html_generation()

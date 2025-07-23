#!/usr/bin/env python3
"""
Project Analysis Script - Determine Actual Filter Maximums
"""
import json
import sys
from pathlib import Path


def analyze_project_maximums():
    """Analyze the current project to determine actual filter maximums"""

    # Load the generated graph data
    try:
        graph_data_path = Path("graph_output/enhanced_graph_data.json")
        if not graph_data_path.exists():
            print("❌ Graph data not found. Run the dependency graph generator first.")
            return None

        with open(graph_data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        nodes = data.get("nodes", [])
        if not nodes:
            print("❌ No nodes found in graph data")
            return None

        # Calculate actual maximums
        max_predecessors = 0
        max_successors = 0
        max_size_kb = 0

        for node in nodes:
            # Count predecessors (incoming edges)
            predecessors = len(
                [
                    edge
                    for edge in data.get("edges", [])
                    if edge["target"] == node["index"]
                ]
            )
            max_predecessors = max(max_predecessors, predecessors)

            # Count successors (outgoing edges)
            successors = len(
                [
                    edge
                    for edge in data.get("edges", [])
                    if edge["source"] == node["index"]
                ]
            )
            max_successors = max(max_successors, successors)

            # File size in KB
            size_kb = node.get("size_kb", 0)
            max_size_kb = max(max_size_kb, size_kb)

        result = {
            "max_predecessors": max_predecessors,
            "max_successors": max_successors,
            "max_size_kb": int(max_size_kb),
            "total_nodes": len(nodes),
            "total_edges": len(data.get("edges", [])),
        }

        print("📊 PROJECT ANALYSIS RESULTS")
        print("=" * 40)
        print(f"📁 Total files analyzed: {result['total_nodes']}")
        print(f"🔗 Total dependencies: {result['total_edges']}")
        print(f"📥 Maximum predecessors: {result['max_predecessors']}")
        print(f"📤 Maximum successors: {result['max_successors']}")
        print(f"📄 Maximum file size: {result['max_size_kb']} KB")
        print()
        print("🎯 RECOMMENDED FILTER MAXIMUMS:")
        print(f"   Predecessors: {result['max_predecessors']}")
        print(f"   Successors: {result['max_successors']}")
        print(f"   File Size: {result['max_size_kb']} KB")

        # Also analyze node names for truncation issues
        long_names = [node for node in nodes if len(node.get("stem", "")) > 10]
        if long_names:
            print(f"\n📝 LONG NODE NAMES ({len(long_names)} files):")
            for node in sorted(
                long_names, key=lambda x: len(x.get("stem", "")), reverse=True
            )[:5]:
                print(f"   {len(node.get('stem', ''))}: {node.get('stem', '')}")

        return result

    except Exception as e:
        print(f"❌ Error analyzing project: {e}")
        return None


if __name__ == "__main__":
    analyze_project_maximums()

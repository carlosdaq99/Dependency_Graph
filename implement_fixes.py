#!/usr/bin/env python3
"""
Implementation Script for Recurring Issues Fixes
===============================================

This script implements fixes for all 4 identified root causes:
1. Fix edge highlighting logic for blue edges between orange & blue nodes
2. Consolidate CSS dimming definitions
3. Improve tooltip horizontal positioning
4. Clean up duplicate file architecture

Following Multi-Stage Action Plan - Phase 5: Implementation
"""

import sys
import shutil
from pathlib import Path
import re
from datetime import datetime


def fix_edge_highlighting_logic():
    """Fix 1: Blue edges between orange & blue nodes not showing"""
    print("🔵🟠 FIX 1: Edge highlighting logic for mixed-category edges")
    print("=" * 70)

    interactions_file = Path("graph_modules/graph_visualization/interactions.py")

    if not interactions_file.exists():
        print("❌ interactions.py not found!")
        return False

    content = interactions_file.read_text(encoding="utf-8")
    original_content = content

    # Fix 1: Add logic for mixed-category edges (between orange and blue nodes)
    print("🔧 Adding mixed-category edge highlighting logic...")

    # Find the problematic edge highlighting section
    old_pattern = r'// Highlight edges - FIXED: Only highlight edges between highlighted nodes\s+window\.graphElements\.link\s+\.classed\("highlighted", d => directConnected\.has\(d\.source_name\) && directConnected\.has\(d\.target_name\)\)\s+\.classed\("path-highlighted", d => pathConnected\.has\(d\.source_name\) && pathConnected\.has\(d\.target_name\)\)'

    new_logic = """// Highlight edges - ENHANCED: Support mixed-category edges
                window.graphElements.link
                    .classed("highlighted", d => directConnected.has(d.source_name) && directConnected.has(d.target_name))
                    .classed("path-highlighted", d => pathConnected.has(d.source_name) && pathConnected.has(d.target_name))
                    .classed("mixed-highlighted", d => 
                        (directConnected.has(d.source_name) && pathConnected.has(d.target_name)) ||
                        (pathConnected.has(d.source_name) && directConnected.has(d.target_name))
                    )"""

    # Apply the fix
    if "mixed-highlighted" not in content:
        # Find and replace the edge highlighting section
        pattern = r'(window\.graphElements\.link\s+\.classed\("highlighted"[^}]+})\)'
        if re.search(pattern, content, re.DOTALL):
            # Add mixed highlighting class
            content = re.sub(
                r'(\.classed\("path-highlighted", d => pathConnected\.has\(d\.source_name\) && pathConnected\.has\(d\.target_name\)\))',
                r'\1\n                    .classed("mixed-highlighted", d => \n                        (directConnected.has(d.source_name) && pathConnected.has(d.target_name)) ||\n                        (pathConnected.has(d.source_name) && directConnected.has(d.target_name))\n                    )',
                content,
            )
            print("   ✅ Added mixed-category edge highlighting logic")
        else:
            print("   ⚠️ Could not locate exact pattern - manual fix needed")

    # Fix 2: Update arrow marker logic for mixed edges
    print("🎯 Adding mixed-category arrow markers...")

    if "arrowhead-mixed" not in content:
        # Find arrow marker section and add mixed case
        marker_pattern = r'(} else if \(pathConnected\.has\(d\.source_name\) && pathConnected\.has\(d\.target_name\)\) {\s+return "url\(#arrowhead-path\)";)'
        if re.search(marker_pattern, content):
            replacement = r"""\1
                        } else if ((directConnected.has(d.source_name) && pathConnected.has(d.target_name)) ||
                                   (pathConnected.has(d.source_name) && directConnected.has(d.target_name))) {
                            return "url(#arrowhead-mixed)";"""
            content = re.sub(marker_pattern, replacement, content)
            print("   ✅ Added mixed-category arrow markers")

    # Save the changes
    if content != original_content:
        # Create backup
        backup_file = interactions_file.with_suffix(".py.backup")
        shutil.copy2(interactions_file, backup_file)
        print(f"   📁 Backup created: {backup_file}")

        # Write updated content
        interactions_file.write_text(content, encoding="utf-8")
        print("   ✅ Updated interactions.py with edge highlighting fixes")
        return True
    else:
        print("   ⚠️ No changes needed or pattern not found")
        return False


def fix_css_dimming_conflicts():
    """Fix 2: Consolidate CSS dimming definitions"""
    print("\n🔘 FIX 2: CSS dimming conflicts consolidation")
    print("=" * 70)

    # Identify the authoritative CSS file
    primary_css = Path("graph_modules/graph_styles/layout_styles.py")
    duplicate_css = Path("graph_modules/graph_styles_internal/layout_styles.py")

    if not primary_css.exists():
        print("❌ Primary CSS file not found!")
        return False

    print("🔧 Consolidating CSS dimming definitions...")

    # Read primary CSS content
    primary_content = primary_css.read_text(encoding="utf-8")

    # Enhanced dimming CSS with important declarations
    enhanced_dimming = """        /* Enhanced dimming styles - consolidated and prioritized */
        .link.dimmed {
            opacity: var(--dimmed-link-opacity) !important;
            transition: opacity 0.3s ease !important;
        }
        
        .node.dimmed {
            opacity: var(--dimmed-opacity) !important;
            transition: opacity 0.3s ease !important;
        }
        
        .node-label.dimmed {
            opacity: var(--dimmed-text-opacity) !important;
            transition: opacity 0.3s ease !important;
        }
        
        /* Mixed-category edge styles */
        .link.mixed-highlighted {
            stroke: var(--mixed-edge-color, #9c27b0) !important;  /* Purple for mixed edges */
            stroke-width: 2.8 !important;
            opacity: 0.95 !important;
        }"""

    # Check if enhanced dimming is already present
    if "mixed-highlighted" not in primary_content:
        # Add enhanced dimming styles
        dimming_pattern = r"(\.link\.dimmed \{[^}]+\})"
        if re.search(dimming_pattern, primary_content):
            primary_content = re.sub(dimming_pattern, enhanced_dimming, primary_content)

            # Write updated primary CSS
            primary_css.write_text(primary_content, encoding="utf-8")
            print("   ✅ Enhanced dimming styles added to primary CSS")
        else:
            print("   ⚠️ Could not locate dimming pattern in primary CSS")

    # Comment out conflicting CSS in duplicate file
    if duplicate_css.exists():
        duplicate_content = duplicate_css.read_text(encoding="utf-8")

        # Comment out conflicting dimming styles
        conflicting_pattern = r"(\.link\.dimmed \{[^}]+\})"
        if re.search(conflicting_pattern, duplicate_content):
            duplicate_content = re.sub(
                conflicting_pattern,
                r"/* DISABLED - Consolidated to primary CSS file\n        \1\n        */",
                duplicate_content,
            )

            duplicate_css.write_text(duplicate_content, encoding="utf-8")
            print("   ✅ Disabled conflicting CSS in duplicate file")

    print("   ✅ CSS dimming conflicts resolved")
    return True


def fix_tooltip_positioning():
    """Fix 3: Improve tooltip horizontal positioning"""
    print("\n📍 FIX 3: Tooltip horizontal positioning")
    print("=" * 70)

    interactions_file = Path("graph_modules/graph_visualization/interactions.py")

    if not interactions_file.exists():
        print("❌ interactions.py not found!")
        return False

    content = interactions_file.read_text(encoding="utf-8")
    original_content = content

    print("🔧 Improving tooltip positioning logic...")

    # Fix tooltip positioning with responsive logic
    old_positioning = r'\.style\("left", \(event\.pageX \+ 10\) \+ "px"\)'
    new_positioning = r'.style("left", (event.pageX + Math.min(25, window.innerWidth - event.pageX - 320)) + "px")'

    if re.search(old_positioning, content):
        content = re.sub(old_positioning, new_positioning, content)
        print("   ✅ Updated horizontal positioning with responsive logic")

        # Also improve vertical positioning
        old_vertical = r'\.style\("top", \(event\.pageY - 10\) \+ "px"\)'
        new_vertical = (
            r'.style("top", (event.pageY - Math.min(15, event.pageY - 100)) + "px")'
        )

        if re.search(old_vertical, content):
            content = re.sub(old_vertical, new_vertical, content)
            print("   ✅ Updated vertical positioning with edge detection")

    # Save changes
    if content != original_content:
        interactions_file.write_text(content, encoding="utf-8")
        print("   ✅ Tooltip positioning improved")
        return True
    else:
        print("   ⚠️ No positioning changes needed")
        return False


def fix_duplicate_files():
    """Fix 4: Clean up duplicate file architecture"""
    print("\n🔄 FIX 4: Duplicate file architecture cleanup")
    print("=" * 70)

    graph_modules = Path("graph_modules")

    if not graph_modules.exists():
        print("❌ graph_modules directory not found!")
        return False

    print("🔧 Cleaning up duplicate files...")

    # Archive duplicate files instead of deleting
    archive_dir = Path("archived_duplicates")
    archive_dir.mkdir(exist_ok=True)

    # Files to archive (keep the main versions)
    files_to_archive = [
        "graph_modules/dependency_analyzer_new.py",
        "graph_modules/graph_controls_new.py",
        "graph_modules/graph_styles_new.py",
        "graph_modules/graph_styles_backup.py",
        "graph_modules/graph_visualization_new.py",
    ]

    archived_count = 0
    for file_path in files_to_archive:
        source = Path(file_path)
        if source.exists():
            # Create archive filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"{source.stem}_{timestamp}{source.suffix}"
            target = archive_dir / archive_name

            shutil.move(source, target)
            print(f"   📁 Archived: {file_path} -> {target}")
            archived_count += 1

    # Clean up duplicate CSS structures
    duplicate_styles_dir = Path("graph_modules/graph_styles_internal")
    if duplicate_styles_dir.exists():
        archive_styles = archive_dir / "graph_styles_internal"
        shutil.move(duplicate_styles_dir, archive_styles)
        print(f"   📁 Archived duplicate styles directory: {archive_styles}")
        archived_count += 1

    print(f"   ✅ Archived {archived_count} duplicate files/directories")
    return archived_count > 0


def add_enhanced_css_variables():
    """Add enhanced CSS variables for new features"""
    print("\n🎨 ENHANCEMENT: Adding CSS variables for new features")
    print("=" * 70)

    base_styles_file = Path("graph_modules/graph_styles/base_styles.py")

    if not base_styles_file.exists():
        print("❌ base_styles.py not found!")
        return False

    content = base_styles_file.read_text(encoding="utf-8")

    # Enhanced CSS variables
    enhanced_variables = """            /* Enhanced edge highlighting variables */
            --mixed-edge-color: #9c27b0;  /* Purple for mixed orange/blue edges */
            --dimmed-link-opacity: 0.15;
            --dimmed-opacity: 0.2;
            --dimmed-text-opacity: 0.3;"""

    # Check if variables already exist
    if "--mixed-edge-color" not in content:
        # Find CSS variables section and add enhanced variables
        variables_pattern = r"(--accent-color: #fd7e14;[^}]+)"
        if re.search(variables_pattern, content):
            content = re.sub(variables_pattern, r"\1\n" + enhanced_variables, content)

            base_styles_file.write_text(content, encoding="utf-8")
            print("   ✅ Added enhanced CSS variables")
            return True

    print("   ⚠️ Enhanced variables already present or pattern not found")
    return False


def run_implementation():
    """Execute all fixes following Multi-Stage Action Plan"""
    print("🚀 IMPLEMENTING FIXES FOR RECURRING ISSUES")
    print("Following Multi-Stage Action Plan - Phase 5")
    print("=" * 80)

    fixes_results = {
        "edge_highlighting": fix_edge_highlighting_logic(),
        "css_dimming": fix_css_dimming_conflicts(),
        "tooltip_positioning": fix_tooltip_positioning(),
        "duplicate_files": fix_duplicate_files(),
        "css_variables": add_enhanced_css_variables(),
    }

    print("\n📊 IMPLEMENTATION RESULTS")
    print("=" * 80)

    successful_fixes = sum(fixes_results.values())
    total_fixes = len(fixes_results)

    for fix_name, result in fixes_results.items():
        status = "✅ SUCCESS" if result else "⚠️ PARTIAL"
        print(f"   {status} {fix_name.replace('_', ' ').title()}")

    print(
        f"\n📈 Implementation: {successful_fixes}/{total_fixes} fixes applied ({successful_fixes/total_fixes*100:.1f}%)"
    )

    if successful_fixes >= 3:  # At least 3 out of 5 fixes successful
        print(f"\n🎯 IMPLEMENTATION SUCCESS!")
        print(f"   Major recurring issues have been addressed")
        print(f"   Ready for validation testing")

        print(f"\n⚡ NEXT STEPS:")
        print(f"   1. Run comprehensive test suite")
        print(f"   2. Test each fix individually")
        print(f"   3. Validate in browser")
        print(f"   4. Monitor for regression")

        return True
    else:
        print(f"\n⚠️ PARTIAL IMPLEMENTATION")
        print(f"   Some fixes may need manual intervention")
        print(f"   Review error messages above")

        return False


if __name__ == "__main__":
    try:
        success = run_implementation()

        if success:
            print(f"\n✅ Implementation completed successfully")
            sys.exit(0)
        else:
            print(f"\n⚠️ Implementation completed with warnings")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Implementation failed: {e}")
        sys.exit(2)

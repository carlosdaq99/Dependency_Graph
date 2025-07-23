"""
Import Resolution Module
=======================

Handles import detection, resolution, and mapping to actual files.
Contains logic for resolving relative imports and mapping imports to file IDs.
"""

import ast
import os
from pathlib import Path
from typing import List, Tuple, Optional


class ImportResolver:
    """Handles import resolution and mapping for dependency analysis."""

    def __init__(self, analyzer):
        """Initialize with reference to the main analyzer."""
        self.analyzer = analyzer

    def extract_imports(
        self, tree: ast.AST, file_path: Path
    ) -> Tuple[List[str], List[str]]:
        """Enhanced import extraction with better resolution."""
        internal_imports = []
        all_imports = []
        current_folder = self.analyzer.get_folder_name(file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    all_imports.append(alias.name)
                    resolved = self.resolve_import_to_file(alias.name, current_folder)
                    if resolved:
                        internal_imports.append(resolved)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module_name = node.module
                    all_imports.append(module_name)

                    # Handle relative imports
                    if module_name.startswith("."):
                        # Relative import - resolve based on current location
                        resolved = self.resolve_relative_import(module_name, file_path)
                        if resolved:
                            internal_imports.append(resolved)
                    else:
                        # Absolute import
                        resolved = self.resolve_import_to_file(
                            module_name, current_folder
                        )
                        if resolved:
                            internal_imports.append(resolved)

        return internal_imports, all_imports

    def resolve_relative_import(
        self, import_name: str, current_file: Path
    ) -> Optional[str]:
        """Resolve relative imports to actual file IDs."""
        # Count dots to determine level
        level = 0
        while level < len(import_name) and import_name[level] == ".":
            level += 1

        if level == 0:
            return None

        # Get the module name after dots
        module_name = import_name[level:] if level < len(import_name) else ""

        # Navigate up the directory tree
        target_dir = current_file.parent
        for _ in range(level - 1):
            target_dir = target_dir.parent

        # If module_name is empty, looking for __init__.py in target_dir
        if not module_name:
            target_file = target_dir / "__init__.py"
        else:
            # Replace dots with path separators
            module_path = module_name.replace(".", os.sep)
            target_file = target_dir / f"{module_path}.py"

            # Also check for __init__.py in directory
            if not target_file.exists():
                target_file = target_dir / module_path / "__init__.py"

        if target_file.exists():
            return self.analyzer.create_unique_id(target_file)

        return None

    def resolve_import_to_file(
        self, import_name: str, current_folder: str
    ) -> Optional[str]:
        """Enhanced import resolution to map imports to actual files."""
        # Check if this import corresponds to any known file
        import_parts = import_name.split(".")

        # Try different combinations to find the actual file
        for unique_id, info in self.analyzer.dependencies.items():
            # Direct stem match
            if info["stem"] == import_parts[0]:
                return unique_id

            # Try matching with folder structure
            if len(import_parts) > 1:
                if (
                    info["folder"] == import_parts[0]
                    and info["stem"] == import_parts[1]
                ):
                    return unique_id

            # Try matching full module path
            file_path = Path(info["file_path"])
            try:
                # Convert file path to module notation
                relative_path = file_path.relative_to(Path("."))
                if relative_path.stem == "__init__":
                    module_path = ".".join(relative_path.parent.parts)
                else:
                    module_path = ".".join(relative_path.with_suffix("").parts)

                if module_path == import_name:
                    return unique_id
            except ValueError:
                pass

        return None

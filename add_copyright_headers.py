#!/usr/bin/env python3
"""
Script to add copyright headers to Python and Shell files in the project.

Usage:
    Add your name in the PYTHON_HEADER and SHELL_HEADER variables below at [Your Name Here].
    Run the script with:
        python add_copyright_headers.py

This will add copyright headers to all .py and .sh files that don't already have them.
"""

import os
from pathlib import Path

# Copyright header template for Python files
PYTHON_HEADER = '''"""
Automated Architecture Discovery System
Copyright (c) 2025 [Your Name Here]

Licensed under the MIT License.
See LICENSE file in the project root for full license information.

This file is part of the Automated Architecture Discovery System,
an educational project demonstrating microservices architecture discovery.
"""

'''

# Copyright header template for Shell files
SHELL_HEADER = '''#
# Automated Architecture Discovery System
# Copyright (c) 2025 [Your Name Here]
#
# Licensed under the MIT License.
# See LICENSE file in the project root for full license information.
#
# This file is part of the Automated Architecture Discovery System,
# an educational project demonstrating microservices architecture discovery.
#

'''

# Files to skip
SKIP_FILES = {
    'add_copyright_headers.py',
    'add_copyright_headers_v2.py',  # This script itself
    '__init__.py',  # Usually keep these minimal
}

# Directories to skip
SKIP_DIRS = {
    'venv',
    '.venv',
    'env',
    '__pycache__',
    '.git',
    'node_modules',
}

def has_copyright_header(file_path):
    """Check if file already has a copyright header."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(500)  # Read first 500 chars
            return 'Copyright (c)' in content or 'Licensed under' in content
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return True  # Assume it has header to avoid modifying

def add_header_to_python_file(file_path):
    """Add copyright header to a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Check if file starts with shebang
        if original_content.startswith('#!'):
            lines = original_content.split('\n', 1)
            shebang = lines[0] + '\n'
            rest = lines[1] if len(lines) > 1 else ''
            new_content = shebang + PYTHON_HEADER + rest
        else:
            new_content = PYTHON_HEADER + original_content
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"Error modifying {file_path}: {e}")
        return False

def add_header_to_shell_file(file_path):
    """Add copyright header to a Shell script file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Check if file starts with shebang
        if original_content.startswith('#!'):
            lines = original_content.split('\n', 1)
            shebang = lines[0] + '\n'
            rest = lines[1] if len(lines) > 1 else ''
            new_content = shebang + SHELL_HEADER + rest
        else:
            # If no shebang, add one
            new_content = '#!/bin/bash\n' + SHELL_HEADER + original_content
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"Error modifying {file_path}: {e}")
        return False

def process_directory(directory='.'):
    """Process all Python and Shell files in directory and subdirectories."""
    directory = Path(directory)
    py_processed = 0
    sh_processed = 0
    skipped = 0
    errors = 0
    
    print("=" * 60)
    print("Adding Copyright Headers to Python and Shell Files")
    print("=" * 60)
    print()
    
    # Process Python files
    print("📝 Processing Python files (.py)...")
    print("-" * 60)
    for py_file in directory.rglob('*.py'):
        # Skip files in excluded directories
        if any(skip_dir in py_file.parts for skip_dir in SKIP_DIRS):
            continue
        
        # Skip specific files
        if py_file.name in SKIP_FILES:
            print(f"⏭️  Skipping: {py_file}")
            skipped += 1
            continue
        
        # Check if already has header
        if has_copyright_header(py_file):
            print(f"✅ Already has header: {py_file}")
            skipped += 1
            continue
        
        # Add header
        print(f"📝 Adding header to: {py_file}")
        if add_header_to_python_file(py_file):
            py_processed += 1
        else:
            errors += 1
    
    print()
    
    # Process Shell files
    print("📝 Processing Shell files (.sh)...")
    print("-" * 60)
    for sh_file in directory.rglob('*.sh'):
        # Skip files in excluded directories
        if any(skip_dir in sh_file.parts for skip_dir in SKIP_DIRS):
            continue
        
        # Check if already has header
        if has_copyright_header(sh_file):
            print(f"✅ Already has header: {sh_file}")
            skipped += 1
            continue
        
        # Add header
        print(f"📝 Adding header to: {sh_file}")
        if add_header_to_shell_file(sh_file):
            sh_processed += 1
        else:
            errors += 1
    
    # Print summary
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"✅ Python headers added: {py_processed}")
    print(f"✅ Shell headers added: {sh_processed}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Errors: {errors}")
    print(f"📊 Total processed: {py_processed + sh_processed}")
    print()

def main():
    """Main function."""
    print("This script will add copyright headers to all Python (.py) and Shell (.sh) files.")
    print("Files that already have copyright headers will be skipped.")
    print()
    print("⚠️  Make sure you've updated the copyright name in this script before running!")
    print("   Current name: Abhishek Datta")
    print()
    
    response = input("Continue? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Cancelled.")
        return
    
    print()
    process_directory()
    
    print("Done! Please review the changes before committing.")
    print("Run 'git diff' to see what changed.")
    print()
    print("💡 Tip: You can also run this script again in the future if you add new files.")

if __name__ == '__main__':
    main()
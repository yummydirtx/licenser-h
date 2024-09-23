# Copyright (c) 2024 Alex Frutkin
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (Licenser), to deal in
# Licenser without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# Licenser, and to permit persons to whom Licenser is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of Licenser.
# 
# LICENSER IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH LICENSER OR THE USE OR OTHER DEALINGS IN LICENSER.

import os
import sys
from detect_license import detect_license
from get_license import get_license_header_patterns

# Mapping of file extensions to their comment styles
comment_styles = {
    '.py': '#',           # Python
    '.sh': '#',           # Shell script
    '.c': '//',           # C
    '.cpp': '//',         # C++
    '.h': '//',           # Header files
    '.java': '//',        # Java
    '.js': '//',          # JavaScript
    '.cs': '//',          # C#
    '.go': '//',          # Go
    '.rb': '#',           # Ruby
    '.php': '//',         # PHP
    '.html': '<!--|-->',  # HTML
    '.xml': '<!--|-->',   # XML
    '.css': '/*|*/',      # CSS
    # Add more extensions as needed
}

def add_license_header(file_path, comment_style, license_lines, license_header_patterns):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.readlines()

    # Check if any supported license header is already present
    result = detect_license(file_path, license_header_patterns, comment_style)
    if result:
        start_line, end_line = result
        # Remove the existing license lines
        content = content[:start_line] + content[end_line + 1:]
        insert_position = start_line
    else:
        insert_position = 0  # Insert at the top if no existing license

    # Create the new license header
    if comment_style in ['#', '//']:
        license_header = [f"{comment_style} {line}\n" for line in license_lines]
    elif comment_style == '/*|*/':
        license_header = ['/*\n'] + [f" * {line}\n" for line in license_lines] + [' */\n']
    elif comment_style == '<!--|-->':
        license_header = ['<!--\n'] + [f"  {line}\n" for line in license_lines] + ['-->\n']
    else:
        print(f"Unknown comment style for {file_path}")
        return

    # Insert the new license header
    content = content[:insert_position] + license_header + ['\n'] + content[insert_position:]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(content)

def process_project_directory(project_path, license_header):
    license_lines = license_header.strip().split('\n')
    license_header_patterns = get_license_header_patterns()

    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file)

            if ext in comment_styles:
                comment_style = comment_styles[ext]
                add_license_header(file_path, comment_style, license_lines, license_header_patterns)


def create_license_file(project_path, license_text_full):
    license_file_path = os.path.join(project_path, 'LICENSE')
    with open(license_file_path, 'w', encoding='utf-8') as f:
        f.write(license_text_full)

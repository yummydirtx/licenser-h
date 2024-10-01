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

import re

def detect_license(file_path, license_header_patterns, comment_style):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.readlines()

    max_lines_to_check = 100  # Limit to the top of the file
    content_to_check = content[:max_lines_to_check]

    # Extract the first comment block
    comment_block_lines = []
    in_comment_block = False
    end_line_index = 0

    for i, line in enumerate(content_to_check):
        stripped_line = line.strip()
        if not stripped_line and in_comment_block:
            # Empty line after comment block
            break
        if not stripped_line and not in_comment_block:
            # Skip empty lines at the top
            continue

        if comment_style in ['#', '//']:
            if stripped_line.startswith(comment_style):
                in_comment_block = True
                comment_content = stripped_line[len(comment_style):].strip()
                comment_block_lines.append(comment_content)
                end_line_index = i
            else:
                if in_comment_block:
                    # End of comment block
                    break
                else:
                    # Non-comment line before comment block
                    return None
        elif comment_style == '/*|*/':
            if '/*' in stripped_line:
                in_comment_block = True
                start_index = stripped_line.find('/*') + 2
                line_content = stripped_line[start_index:].strip('*').strip()
                comment_block_lines.append(line_content)
                end_line_index = i
                continue
            if '*/' in stripped_line and in_comment_block:
                end_index = stripped_line.find('*/')
                line_content = stripped_line[:end_index].strip('*').strip()
                comment_block_lines.append(line_content)
                end_line_index = i
                break
            if in_comment_block:
                line_content = stripped_line.strip('*').strip()
                comment_block_lines.append(line_content)
                end_line_index = i
            else:
                return None
        elif comment_style == '<!--|-->':
            if '<!--' in stripped_line:
                in_comment_block = True
                start_index = stripped_line.find('<!--') + 4
                line_content = stripped_line[start_index:].strip()
                comment_block_lines.append(line_content)
                end_line_index = i
                continue
            if '-->' in stripped_line and in_comment_block:
                end_index = stripped_line.find('-->')
                line_content = stripped_line[:end_index].strip()
                comment_block_lines.append(line_content)
                end_line_index = i
                break
            if in_comment_block:
                line_content = stripped_line.strip()
                comment_block_lines.append(line_content)
                end_line_index = i
            else:
                return None
        else:
            print(f"Unknown comment style for {file_path}")
            return None

    if not comment_block_lines:
        return None

    # Combine the comment block lines into a single string
    comment_block_text = '\n'.join(comment_block_lines).strip()

    # Try matching against each license header pattern
    for license_key, pattern in license_header_patterns.items():
        regex = re.compile(pattern, re.DOTALL)
        if regex.match(comment_block_text):
            # Found a matching license header
            start_line = 0  # Since we started from the top
            end_line = end_line_index

            # Include all consecutive empty lines after the license block
            next_line_index = end_line_index + 1
            while next_line_index < len(content):
                next_line = content[next_line_index]
                if not next_line.strip():
                    # Next line is empty; include it
                    end_line = next_line_index
                    next_line_index += 1
                else:
                    break  # Non-empty line encountered

            return start_line, end_line

    return None

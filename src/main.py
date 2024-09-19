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

import sys
from .add_license import process_project_directory, create_license_file
import argparse
from .choose_license import choose_license, get_user_info
from .get_license import get_license_texts


def main():
    parser = argparse.ArgumentParser(description='Add license headers to source files and create a LICENSE file.')
    parser.add_argument('project_path', help='Path to the project directory')
    parser.add_argument('--interactive', '-i', action='store_true', help='Enable interactive mode to select license')
    args = parser.parse_args()

    project_path = args.project_path

    if args.interactive:
        license_type = choose_license()
        project_name, author_name = get_user_info()
    else:
        parser.add_argument('--license', '-l', choices=['mit', 'apache2', 'gpl3', 'bsd2'], default='mit',
                            help='License type to apply (default: mit)')
        parser.add_argument('--project_name', '-p', help='Project name')
        parser.add_argument('--author_name', '-a', help='Author name')
        args = parser.parse_args()
        license_type = args.license
        project_name = args.project_name
        author_name = args.author_name

    # Load the selected license texts
    license_text_full, license_header = get_license_texts(license_type, project_name, author_name)

    process_project_directory(project_path, license_header)
    create_license_file(project_path, license_text_full)
    print(f"License headers added and LICENSE file created using the {license_type.upper()} license.")

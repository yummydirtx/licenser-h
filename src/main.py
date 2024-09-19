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

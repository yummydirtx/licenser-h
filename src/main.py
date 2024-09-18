import sys
from add_license import process_project_directory, create_license_file
import argparse
from InquirerPy import inquirer


def main():
    if len(sys.argv) != 2:
        print("Usage: python add_license.py /path/to/project")
        sys.exit(1)

    project_path = sys.argv[1]
    process_project_directory(project_path)
    create_license_file(project_path)
    print("License headers added and LICENSE file created.")

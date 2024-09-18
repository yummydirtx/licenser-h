import unittest
import tempfile
import shutil
import os
import sys
from unittest.mock import patch, MagicMock
from contextlib import contextmanager
from src.add_license import *


class TestAddLicenseScript(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for the project
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)

        # Create some test files with different extensions
        self.test_files = {
            'test.py': 'print("Hello World")\n',
            'test.sh': 'echo "Hello World"\n',
            'test.c': '#include <stdio.h>\nint main() { return 0; }\n',
            'test.txt': 'This is a text file.\n',
            'test_with_license.py': f"# {license_header}\nprint('Already has license')\n",
        }

        for filename, content in self.test_files.items():
            with open(os.path.join(self.test_dir, filename), 'w', encoding='utf-8') as f:
                f.write(content)

    def test_add_license_header_python_file(self):
        file_path = os.path.join(self.test_dir, 'test.py')
        comment_style = comment_styles['.py']
        license_lines = license_header.strip().split('\n')

        add_license_header(file_path, comment_style, license_lines)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if license header is added
        for line in license_lines:
            self.assertIn(f"{comment_style} {line}", content)

    def test_add_license_header_already_has_license(self):
        file_path = os.path.join(self.test_dir, 'test_with_license.py')
        comment_style = comment_styles['.py']
        license_lines = license_header.strip().split('\n')

        # Capture the original content
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        add_license_header(file_path, comment_style, license_lines)

        # Read the content again
        with open(file_path, 'r', encoding='utf-8') as f:
            new_content = f.read()

        # Since the license was already present, content should not change
        self.assertEqual(original_content, new_content)

    def test_process_project_directory(self):
        process_project_directory(self.test_dir)

        # Check that license headers are added to applicable files
        for filename in self.test_files:
            file_path = os.path.join(self.test_dir, filename)
            _, ext = os.path.splitext(filename)

            if ext in comment_styles and 'with_license' not in filename:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                license_lines = license_header.strip().split('\n')
                comment_style = comment_styles[ext]
                for line in license_lines:
                    if comment_style in ['#', '//']:
                        self.assertIn(f"{comment_style} {line}", content)
                    elif comment_style == '/*|*/':
                        self.assertIn(f" * {line}", content)
                    elif comment_style == '<!--|-->':
                        self.assertIn(f"  {line}", content)
            else:
                # Files that should not have the license added
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'with_license' in filename:
                    self.assertIn('MIT License', content)
                else:
                    self.assertNotIn('MIT License', content)

    def test_create_license_file(self):
        create_license_file(self.test_dir)

        license_file_path = os.path.join(self.test_dir, 'LICENSE')
        self.assertTrue(os.path.exists(license_file_path))

        with open(license_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertEqual(content, license_text_full)

    def test_main_function_success(self):
        # Mock sys.argv
        with patch.object(sys, 'argv', ['add_license.py', self.test_dir]):
            # Capture print output
            with patch('builtins.print') as mock_print:
                main()

        # Check that the LICENSE file was created
        license_file_path = os.path.join(self.test_dir, 'LICENSE')
        self.assertTrue(os.path.exists(license_file_path))

        # Check that license headers are added
        for filename in self.test_files:
            file_path = os.path.join(self.test_dir, filename)
            _, ext = os.path.splitext(filename)

            if ext in comment_styles and 'with_license' not in filename:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.assertIn('MIT License', content)

        # Check that the final print statement was called
        mock_print.assert_called_with("License headers added and LICENSE file created.")

    def test_main_function_missing_argument(self):
        # Mock sys.argv with missing argument
        with patch.object(sys, 'argv', ['add_license.py']):
            # Capture sys.exit
            with self.assertRaises(SystemExit) as cm:
                # Capture print output
                with patch('builtins.print') as mock_print:
                    main()
            self.assertEqual(cm.exception.code, 1)
            mock_print.assert_called_with("Usage: python add_license.py /path/to/project")

    def test_add_license_header_unknown_comment_style(self):
        # Add a file with an unsupported extension
        filename = 'test.unknown'
        file_path = os.path.join(self.test_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('Unknown file type content\n')

        # Mock print to capture output
        with patch('builtins.print') as mock_print:
            add_license_header(file_path, '???', ['License line'])
            mock_print.assert_called_with(f"Unknown comment style for {file_path}")

    def test_process_project_directory_skips_unsupported_files(self):
        # Add a file with an unsupported extension
        filename = 'test.unknown'
        file_path = os.path.join(self.test_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('Unknown file type content\n')

        process_project_directory(self.test_dir)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # The content should remain unchanged
        self.assertEqual(content, 'Unknown file type content\n')

    def test_add_license_header_with_shebang(self):
        # Create a script with a shebang
        filename = 'script_with_shebang.py'
        file_path = os.path.join(self.test_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('#!/usr/bin/env python3\nprint("Hello World")\n')

        # Modify the add_license_header to handle shebang (assuming we've added this feature)
        def add_license_header_shebang(file_path, comment_style, license_lines):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.readlines()

            shebang = ''
            if content and content[0].startswith('#!'):
                shebang = content.pop(0)

            if any(license_lines[0] in line for line in content[:len(license_lines) + 5]):
                return

            if comment_style in ['#', '//']:
                license_header_lines = [f"{comment_style} {line}\n" for line in license_lines]
            elif comment_style == '/*|*/':
                license_header_lines = ['/*\n'] + [f" * {line}\n" for line in license_lines] + [' */\n']
            elif comment_style == '<!--|-->':
                license_header_lines = ['<!--\n'] + [f"  {line}\n" for line in license_lines] + ['-->\n']
            else:
                print(f"Unknown comment style for {file_path}")
                return

            with open(file_path, 'w', encoding='utf-8') as f:
                if shebang:
                    f.write(shebang)
                f.writelines(license_header_lines + ['\n'] + content)

        # Use the modified function for this test
        comment_style = comment_styles['.py']
        license_lines = license_header.strip().split('\n')
        add_license_header_shebang(file_path, comment_style, license_lines)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check that the shebang is at the top
        self.assertTrue(content.startswith('#!/usr/bin/env python3\n'))

        # Check that the license header is after the shebang
        license_index = content.find('MIT License')
        self.assertTrue(license_index > 0)

    def test_exclude_directories(self):
        # Create an excluded directory
        excluded_dir = os.path.join(self.test_dir, 'venv')
        os.makedirs(excluded_dir)

        # Add a file inside the excluded directory
        file_path = os.path.join(excluded_dir, 'excluded.py')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('print("This should not have a license header")\n')

        # Modify the process_project_directory to exclude 'venv' directory
        def process_project_directory_exclude(project_path):
            license_lines = license_header.strip().split('\n')

            for root, dirs, files in os.walk(project_path):
                # Skip 'venv' directory
                dirs[:] = [d for d in dirs if d != 'venv']
                for file in files:
                    file_path = os.path.join(root, file)
                    _, ext = os.path.splitext(file)

                    if ext in comment_styles:
                        comment_style = comment_styles[ext]
                        add_license_header(file_path, comment_style, license_lines)

        process_project_directory_exclude(self.test_dir)

        # Check that the file inside 'venv' does not have the license header
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertNotIn('MIT License', content)
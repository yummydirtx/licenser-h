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

from InquirerPy import inquirer

def choose_license():
    license_choices = [
        {"name": "MIT License", "value": "mit"},
        {"name": "Apache License 2.0", "value": "apache2"},
        {"name": "GNU General Public License v3.0", "value": "gpl3"},
        {"name": "BSD 2-Clause Simplified License", "value": "bsd2"},
    ]

    license_type = inquirer.select(
        message="Select a license:",
        choices=license_choices,
        default="mit",
    ).execute()

    return license_type

def get_user_info():
    questions = [
        inquirer.text(message="Enter the project name:").execute(),
        inquirer.text(message="Enter the author name:").execute(),
    ]

    return questions[0], questions[1]

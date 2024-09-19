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

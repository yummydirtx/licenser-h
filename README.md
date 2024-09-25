# licenser-h

A Python tool to add or update license headers in your project files.

## Description 

licenser-h is a command-line utility designed to automate the process of adding or updating licenses and license headers in your project's source code files. It supports multiple programming languages and license types, ensuring that your code complies with the licensing requirements of your choice.

## Features 
 
- **Supports Multiple Licenses** :
  - MIT License

  - Apache License 2.0

  - GNU General Public License v3.0

  - BSD 2-Clause Simplified License
 
- **Multi-language Support** :
  - Python, Shell Script, C, C++, Java, JavaScript, C#, Go, Ruby, PHP, HTML, XML, CSS, and more.
 
- **Automatic Detection and Replacement** :
  - Detects existing license headers and replaces them.

  - Only updates the license header at the top of the file without affecting other comments.
 
- **Customizable Placeholders** : 
  - Inserts custom values representing the current year, project name, and author name.

## Installation 

### Prerequisites 

- Python 3.6 or higher
 
- `pip` package manager
Using `setup.py` You can install licenser-h by cloning the repository and running the `setup.py` script:

```bash
# Clone the repository
git clone https://github.com/yummydirtx/licenser-h.git
cd licenser-h

# Install the package
python -m pip install .
```
Using `pip`
licenser-h is available on PyPI, you can install it directly:


```bash
pip install licenser-h
```
## Usage 

### Command-Line Interface 

Run the licenser-h tool from your command line:


```bash
licenser-h
```

#### Example Interaction 


```mathematica
Enter the project name: MyAwesomeProject
Enter the author name: Jane Doe
Select a license:
  ❯ MIT License
    Apache License 2.0
    GNU General Public License v3.0
    BSD 2-Clause Simplified License
```

After providing the necessary information, licenser-h will:
 
- Generate a `LICENSE` file in your project's root directory.

- Add or update license headers in all supported source code files within your project.

### Supported File Extensions 

licenser-h automatically detects files with the following extensions:
 
- **Script Languages** : `.py`, `.sh`, `.rb`, `.php`
 
- **Compiled Languages** : `.c`, `.cpp`, `.h`, `.java`, `.cs`, `.go`
 
- **Web Technologies** : `.js`, `.html`, `.xml`, `.css`
 
- **Others** : Additional language support is coming!

## How It Works 
 
1. **License Selection** : Prompts you to select a license from the supported options.
 
2. **User Information** : Asks for the project name and author name.
 
3. **License Text Generation** : Uses the provided information to generate the full license text and license header, replacing placeholders.
 
4. **File Processing** :
  - Walks through the project directory.

  - Detects files with supported extensions.

  - Adds or updates the license header at the top of each file.
 
5. **Existing License Detection** :
  - Detects existing license headers by matching patterns, even if placeholder values are unknown.

  - Replaces the old license header with the new one without affecting other comments or code.

## License 
This project is licensed under the MIT License - see the LICENSE file for details.
## Contributing 

Contributions are welcome! If you have suggestions for improvements or encounter any issues, please feel free to open an issue or submit a pull request.

### Steps to Contribute 

1. Fork the repository.

2. Create a new branch for your feature or bugfix.

3. Commit your changes with descriptive messages.

4. Push the branch to your forked repository.

5. Open a pull request against the main branch.

## Contact 
For questions or support, please contact [theJunkyard webadmin](mailto:support@thejunkyard.dev).

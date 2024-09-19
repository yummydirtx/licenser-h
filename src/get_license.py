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

from datetime import datetime
from .full_licenses import licenses_text_full, license_headers


def get_license_texts(license_type, project_name, author_name):
    # Define the license text for the LICENSE file
    current_year = datetime.now().year
    project_name_caps = project_name.upper()
    license_text_full = licenses_text_full[license_type].replace("|year|", str(current_year)).replace("|author|", author_name).replace("|projectname|", project_name).replace("|projectnamecaps|", project_name_caps)
    license_header = license_headers[license_type].replace("|year|", str(current_year)).replace("|author|", author_name).replace("|projectname|", project_name).replace("|projectnamecaps|", project_name_caps)
    return license_text_full, license_header

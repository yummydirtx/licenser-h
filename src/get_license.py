from datetime import datetime
from .full_licenses import licenses_text_full, license_headers


def get_license_texts(license_type, project_name, author_name):
    # Define the license text for the LICENSE file
    current_year = datetime.now().year
    project_name_caps = project_name.upper()
    license_text_full = licenses_text_full[license_type].replace("|year|", str(current_year)).replace("|author|", author_name).replace("|projectname|", project_name).replace("|projectnamecaps|", project_name_caps)
    license_header = license_headers[license_type].replace("|year|", str(current_year)).replace("|author|", author_name).replace("|projectname|", project_name).replace("|projectnamecaps|", project_name_caps)
    return license_text_full, license_header

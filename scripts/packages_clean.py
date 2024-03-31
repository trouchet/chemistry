import re

def find_packages_with_comment(requirements_txt):
    """
    Finds packages with the comment '# via -r requirements.txt' in a specified format.
    """
    pattern = r"^package_name==[0-9.]+\n# via -r requirements.txt$"
    with open(requirements_txt, "r") as file:
        for line in file:
            if re.match(pattern, line):
                package_name = line.split("==")[0].strip()
                print(package_name)

# Example usage
find_packages_with_comment("requirements-minimal.txt")
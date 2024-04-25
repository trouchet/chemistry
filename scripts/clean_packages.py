import re
import argparse
import subprocess
import os

def run_pip_compile(
    input_file: str, 
    output_file: str
) -> None:
    '''
    Função para roda pip-compile programaticamente
    '''
    
    # Command to run pip-compile
    command = [
        "pip-compile",
        input_file,
        f"--output-file={output_file}",
        "--quiet",
        "--strip-extras"
    ]

    # Run the command
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running pip-compile: {e}")
        raise
        
def find_packages_with_comment(
    requirements_file: str,
    pip_compile_output_file: str, 
    requirements_output_file: str
):
    """
    Encontra pacores com comentario '# via -r requirements.in' em formato específico.
    """
    splitted_file = requirements_file.split('.')
    name = splitted_file[0]
    extension = splitted_file[1]
    pattern = rf"^([^\s#][\w\-]+)==([\d\.]+)\n\s+# via -r {escape(name)}.{escape(extension)}$"

    with open(pip_compile_output_file, "r") as file:
        with open(requirements_output_file, "w") as out_file:
            text = file.read()
            
            matches = re.finditer(pattern, text, re.MULTILINE)
            
            for match in matches:
                # Catched patterns
                package_name = match.group(1)
                version = match.group(2)
                
                # Write to file
                out_file.write(package_name + '==' + version + "\n")


if __name__ == "__main__":
    description = "Find packages with a specific comment in a requirements file."

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("requirements_file", type=str, help="Path to the requirements file.")
    parser.add_argument("output_file", type=str, help="Path to the output file.")
    
    args = parser.parse_args()

    # Temporary file for pip-compile output
    tmp_file = 'tmp.in'

    run_pip_compile(args.requirements_file, tmp_file)
    find_packages_with_comment(args.requirements_file, tmp_file, args.output_file)

    os.remove(tmp_file)
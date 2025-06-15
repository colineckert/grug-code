import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found'

    if not target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'

    try:
        result = subprocess.run(['python', target_file], cwd=abs_working_dir,
                                timeout=30, capture_output=True, text=True)

        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        if not result.stdout and not result.stderr:
            return "No output produced"

        output = f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        if result.returncode != 0:
            output += f"\nProcess exited with code {result.returncode}"
        return output.strip()
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
        },
    ),
)

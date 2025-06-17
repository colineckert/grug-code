from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {
              function_call_part.name}({function_call_part.args})")

    args = function_call_part.args
    args["working_directory"] = "./calculator"

    function_name = function_call_part.name
    function_result = None
    # Call the function based on its name
    if function_name == "get_files_info":
        from functions.get_files_info import get_files_info
        function_result = get_files_info(**args)

    elif function_name == "get_file_content":
        from functions.get_file_content import get_file_content
        function_result = get_file_content(**args)

    elif function_name == "write_file":
        from functions.write_file import write_file
        function_result = write_file(**args)

    elif function_name == "run_python_file":
        from functions.run_python_file import run_python_file
        function_result = run_python_file(**args)

    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {
                        function_call_part.name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

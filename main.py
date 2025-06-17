import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()

    args = [arg for arg in sys.argv[1:] if arg != "--verbose"]
    verbose = "--verbose" in sys.argv
    user_prompt = " ".join(args)

    if not args:
        print("Grug Code Assistant")
        print("Usage: python main.py <input_text>")
        exit(1)

    user_prompt = " ".join(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose=False):
    model_name = 'gemini-2.0-flash-001'

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if len(response.function_calls) > 0:
        print("Function calls:")
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)
            if function_call_result.parts and function_call_result.parts[0].function_response and function_call_result.parts[0].function_response.response:
                if verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}")
            else:
                raise Exception(f"Function {function_call.name} failed")
    if verbose:
        print("User prompt:", messages[0].parts[0].text)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print(
            "Response tokens:", response.usage_metadata.candidates_token_count
        )


if __name__ == "__main__":
    main()

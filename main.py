import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


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
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages
    )
    print(response.text)

    if verbose:
        print("User prompt:", messages[0].parts[0].text)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print(
            "Response tokens:", response.usage_metadata.candidates_token_count
        )


if __name__ == "__main__":
    main()

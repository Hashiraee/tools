import sys
import argparse
import tiktoken


def num_tokens_openai(string: str, model: str = "gpt-4o") -> int:
    """Returns the number of tokens in a text string using OpenAI's tokenizer."""
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))

    return num_tokens


def main():
    parser = argparse.ArgumentParser(description="Count tokens in a file using OpenAI or Anthropic tokenizer.")
    parser.add_argument("file_name", help="Path to the file to be processed")
    args = parser.parse_args()

    file_name = args.file_name
    file_encoding = "utf-8"

    try:
        with open(file_name, "r", encoding=file_encoding) as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Error reading file: {e}")
        print("Check if the file encoding is correct.")
        sys.exit(1)

    num_tokens = num_tokens_openai(content, "gpt-4o")
    print(f"Number of tokens: {num_tokens}")


if __name__ == "__main__":
    main()

import os
import argparse
import fnmatch


def get_ignored_patterns(directory):
    fileignore_path = os.path.join(directory, '.fileignore')
    if not os.path.exists(fileignore_path):
        return []

    with open(fileignore_path, "r") as file:
        patterns = file.read().splitlines()
        return [pattern.strip() for pattern in patterns if pattern.strip() and not pattern.startswith("#")]


def should_ignore(path, base_path, ignored_patterns):
    rel_path = os.path.relpath(path, base_path)
    for pattern in ignored_patterns:
        if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(rel_path), pattern):
            return True

    return False


def concat_files(directory, output_file, ignored_patterns):
    with open(output_file, "w", encoding='utf-8') as outfile:
        outfile.write("<documents>\n")
        first_file = True
        
        file_index = 1
        for root, dirs, files in os.walk(directory):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), directory, ignored_patterns)]
            
            for file in files:
                file_path = os.path.join(root, file)
                if not should_ignore(file_path, directory, ignored_patterns):
                    if not first_file:
                        outfile.write("\n")
                    else:
                        first_file = False
                    rel_path = os.path.relpath(file_path, directory)
                    # Add the index attribute to the document tag
                    outfile.write(f'  <document index="{file_index}">\n')
                    outfile.write(f"    <source>{rel_path}</source>\n")
                    outfile.write(f"    <document_content>\n")
                    try:
                        with open(file_path, "r", encoding='utf-8') as infile:
                            for line in infile:
                                outfile.write(f"      {line}")
                    except UnicodeDecodeError:
                        outfile.write("      [Error: Unable to read file content]\n")
                    outfile.write(f"    </document_content>\n")
                    outfile.write(f"  </document>")
                    file_index += 1

        outfile.write("\n</documents>\n")


def main():
    parser = argparse.ArgumentParser(description="Concatenate files from a directory into a single XML-like file.")
    parser.add_argument("-f", "--folder", required=True, help="Directory containing the files to concatenate.")
    parser.add_argument("-o", "--output", required=True, help="Output file path.")
    args = parser.parse_args()

    directory = os.path.abspath(args.folder)
    output_file = args.output

    ignored_patterns = get_ignored_patterns(directory)
    concat_files(directory, output_file, ignored_patterns)
    print(f"Files concatenated successfully, output file: {output_file}")


if __name__ == "__main__":
    main()

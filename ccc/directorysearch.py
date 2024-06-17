import os
import re

directory = "C:\\Users\\dad\\Desktop\\three_portfilio"
ignore_list = [
    'node_modules', 
    '.git', 
    '.env',
    'conversations',
    'client/js',
    'client/images',
    'client/icons',
    'program_structure.txt',
    'package-lock.json', 
    'package.json',
    'app2.js'
]

ignore_dirs = {item for item in ignore_list if not '.' in item}
ignore_files = {item for item in ignore_list if '.' in item}

def should_ignore(path, ignore_dirs, ignore_files):
    # Check if the path is in any ignored directory
    for ignore_dir in ignore_dirs:
        if ignore_dir in path.replace("\\", "/"):  # Use forward slash for consistency
            return True
    # Check if the path is in the ignored files
    return any(os.path.basename(path) == ignore_file for ignore_file in ignore_files)

def get_files(directory, ignore_dirs, ignore_files):
    result_files = []
    for root, dirs, files in os.walk(directory):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), ignore_dirs, ignore_files)]
        for file in files:
            file_path = os.path.join(root, file)
            if not should_ignore(file_path, ignore_dirs, ignore_files):
                result_files.append(file_path)
    return result_files

def generate_tree(files, base_dir):
    tree = {}
    for file in files:
        relative_path = os.path.relpath(file, base_dir)
        parts = relative_path.split(os.sep)
        current_level = tree
        for part in parts[:-1]:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        current_level[parts[-1]] = None
    return tree

def print_tree(tree, prefix=''):
    lines = []
    for key, value in sorted(tree.items()):
        lines.append(f"{prefix}├── {key}")
        if isinstance(value, dict):
            lines.extend(print_tree(value, prefix + '    '))
    return lines

def write_directory_structure(filename, directory_structure):
    heading = "\n\n# Project Directory Structure\n"
    heading += "This document details the structure of the project directory, including all directories and files.\n\n"
    heading += "Below, you will find a comprehensive listing of the project's current directory structure and its file contents, including code and filenames.\n\n"

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(heading)
        file.write('\n'.join(directory_structure) + "\n\n")

def append_file_contents(filename, files_list):
    with open(filename, 'a', encoding='utf-8') as file:
        for file_path in files_list:
            relative_path = os.path.relpath(file_path, os.path.dirname(os.path.abspath(__file__)))
            file.write(f"\n# The contents of {relative_path}:\n")
            file.write("\n\n")
            try:
                with open(file_path, 'r', encoding='utf-8') as content_file:
                    file.write(content_file.read())
            except Exception as e:
                file.write(f"Error reading file: {str(e)}")
            file.write("\n\n\n")

def trim_excessive_newlines(text):
    # Reduce occurrences of 4 or more consecutive newlines to just 2
    return re.sub(r'\n{4,}', '\n\n', text)

# Get all files that are not in ignored directories or files
all_files = get_files(directory, ignore_dirs, ignore_files)

# Generate the tree structure
file_tree = generate_tree(all_files, directory)

# Print the tree structure to a list of lines
tree_lines = print_tree(file_tree)

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the output file path
output_file = os.path.join(script_dir, 'file_structure.txt')

# Write the directory structure to the file
write_directory_structure(output_file, tree_lines)

# Append the contents of each file to the file
append_file_contents(output_file, all_files)

# Read the file, trim excessive newlines, and write back the trimmed content
with open(output_file, 'r', encoding='utf-8') as file:
    content = file.read()

trimmed_content = trim_excessive_newlines(content)

with open(output_file, 'w', encoding='utf-8') as file:
    file.write(trimmed_content)

print(f"File structure and contents have been written to {output_file}")

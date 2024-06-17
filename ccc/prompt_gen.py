import os

def create_directory_structure(directory, files):
    result = []
    relative_files = [os.path.relpath(file, directory) for file in files]
    relative_files.sort()
    
    for file in relative_files:
        parts = file.split(os.sep)
        indent = 0
        path_so_far = ""
        for part in parts:
            path_so_far = os.path.join(path_so_far, part)
            if os.path.isdir(path_so_far):
                if '├── ' + part not in result:
                    result.append('    ' * indent + '├── ' + part)
            else:
                if '    ' * indent + '├── ' + part not in result:
                    result.append('    ' * indent + '├── ' + part)
            indent += 1
    
    return result, files

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
            file.write(f"\n#The contents of {relative_path}:\n")
            file.write("\n\n")
            try:
                with open(file_path, 'r', encoding='utf-8') as content_file:
                    file.write(content_file.read())
            except Exception as e:
                file.write(f"Error reading file: {str(e)}")
            file.write("\n\n\n")

def main():
    files_list = [
        # List the files you want to process here
        'index.html',
        'newui.py',
        #'function.py',
        #'ui/script.js',
        #'ui/styles.css'


        # Add more files as needed
    ]
    filename = 'program_structure.txt'
    directory = os.path.dirname(os.path.abspath(__file__))
    
    directory_structure, files_left = create_directory_structure(directory, files_list)
    write_directory_structure(filename, directory_structure)
    append_file_contents(filename, files_left)

if __name__ == "__main__":
    main()

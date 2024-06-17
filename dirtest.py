import os
import sys

AUDIO_EXTENSIONS = {'.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma', '.m4a'}
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'}

def is_audio_file(filename):
    return any(filename.lower().endswith(ext) for ext in AUDIO_EXTENSIONS)

def is_image_file(filename):
    return any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)

def scan_directory(directory, indent=0, ignore=[]):
    result = []
    files_list = []
    for item in sorted(os.listdir(directory)):
        path = os.path.join(directory, item)
        if any(item == ignore_item or path.startswith(os.path.join(directory, ignore_item)) for ignore_item in ignore):
            continue
        if os.path.isdir(path):
            result.append('    ' * indent + '├── ' + item)
            sub_result, sub_files_list = scan_directory(path, indent + 1, ignore)
            result.extend(sub_result)
            files_list.extend(sub_files_list)
        else:
            result.append('    ' * indent + '├── ' + item)
            files_list.append(path)
    return result, files_list

def create_directory_structure(directory, filename, ignore=[]):
    script_name = os.path.basename(__file__)
    
    if script_name not in ignore:
        ignore.append(script_name)
    
    directory_structure, files_list = scan_directory(directory, ignore=ignore)
    
    with open(filename, 'w', encoding='utf-8') as file:
        instructions = (
            "Only show files you edit.\n"
            "This is the current version of the project directory and its file contents.\n\n"
        )
        heading = "Directory Structure of the Project\n"
        heading += "This file contains a structured listing of all directories and files within the project. Contents are included for specified files.\n\n"
        file.write(instructions)
        file.write(heading)
        file.write('\n'.join(directory_structure) + "\n\n")
    
    return files_list

def append_file_contents(filename, files_list):
    with open(filename, 'a', encoding='utf-8') as file:
        for file_path in files_list:
            relative_path = os.path.relpath(file_path, os.path.dirname(os.path.abspath(__file__)))
            if is_audio_file(file_path):
                file.write(f"{relative_path} is a sound file.\n")
            elif is_image_file(file_path):
                file.write(f"{relative_path} is an image file.\n")
            else:
                file.write(f"Contents of {relative_path}:\n")
                file.write("--- start -----------------------\n\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as content_file:
                        file.write(content_file.read())
                except Exception as e:
                    file.write(f"Error reading file: {str(e)}")
                file.write("\n\n--- end -----------------------\n\n\n")

def main():
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
    filename = 'program_structure.txt'
    files_left = create_directory_structure(directory, filename, ignore_list)
    append_file_contents(filename, files_left)

if __name__ == "__main__":
    main()

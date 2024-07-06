import pyttsx3
import sqlite3
import json
import time
import os
from datetime import datetime
import requests
import urllib.request
import pprint
import threading
import markdown
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
pp = pprint.PrettyPrinter(indent=0)

def update_json_file(key, value, filename='site/data.json'):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Initialize data
    data = {}
    
    # Load existing data if the file exists
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
    
    # Update the key with the new value
    data[key] = value
    
    # Save the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
        
    print(f"Updated {filename} with {key}: {value}")


def load_json_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading JSON from file '{file_path}': {e}")
        return None

def pretty_json(json_data):
    try:
        print(json.dumps(json_data, indent=4))
    except TypeError as e:
        print("Error printing JSON:", e)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def jprint(json_obj):
    """
    Pretty print JSON object.

    Args:
        json_obj: JSON object to be pretty printed.
    """
    print(json.dumps(json_obj, indent=4))

def wait(s):
    time.sleep(s)

def split_by_identifier(filename, identifier='=='):
    with open(filename, 'r') as file:
        return file.read().split(identifier)

def save_response_to_file(filename, response):
    with open(filename, "w") as file:
        file.write(response)
    print(f'Done creating {filename}\n')

def read_lines_as_array(file_name):
    try:
        with open(file_name, 'r') as file:
            return [line.lstrip("-").strip() for line in file]
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return []

def concatenate_files(dir_path, output_file):
    files = sorted([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))], key=lambda x: int(''.join(filter(str.isdigit, x))))
    with open(output_file, 'w') as out_file:
        for file_name in files:
            with open(os.path.join(dir_path, file_name), 'r') as in_file:
                out_file.write(in_file.read().strip() + "\n\n")

def load_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None

def save_strings_to_file(string1, string2, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(f"{string1.strip()}\n\n{string2.strip()}")
        print("Strings saved to file successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def save_json(data, filename):
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"Failed to write data to {filename}: {e}")

def start_thread(var, *args):
    threading.Thread(target=var, args=(args), daemon=True).start()

def to_json(fn, content):
    with open(fn, 'w+') as outfile:
        json.dump(content, outfile)

def get_json(url):
    response = urllib.request.urlopen(url)
    return json.loads(response.read().decode("utf8"))

def getjson(file):
    try:
        with open(file) as data_file:
            return json.load(data_file)
    except:
        return {}

def fnbr(n):
    return format(float(n), ".9f")

def formatusd(n):
    return format(float(n), ".2f")

def formatsatoshi(n):
    return format(float(n) * 100000000, ".0f")

def unformatsatoshi(n):
    return format(float(n) / 100000000, ".9f")

def getdate():
    return time.strftime("%d/%m/%Y")

def tofile(filename, content):
    with open(filename, 'a') as fob:
        fob.write(content)

def tonewfile(filename, content):
    with open(filename, 'w+') as fob:
        fob.write(content)

def readfile(fn):
    with open(fn) as f:
        return f.readlines()

def timestamptodate(timestamp):
    return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %I:%M %p')

def makeadir(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)
        print('Dir created')
    else:
        print('Dir already exists')

def getallfiles(directory):
    return [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"File '{filename}' has been deleted.")
    else:
        print(f"File '{filename}' does not exist.")

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B", "0KB", "0MB", "0GB"
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024
    size_gb = size_mb / 1024
    return f"{size_bytes}B", f"{size_kb:.2f}KB", f"{size_mb:.2f}MB", f"{size_gb:.2f}GB"

def get_file_size(file_path):
    try:
        size = os.path.getsize(file_path)
        return convert_size(size)
    except OSError as e:
        print(f"Error: {e}")
        return None

def display_file_size(file_path):
    file_sizes = get_file_size(file_path)
    if file_sizes is not None:
        byte_size, kb_size, mb_size, gb_size = file_sizes
        print(f"The size of '{file_path}' is {byte_size} (bytes), {kb_size} (KB), {mb_size} (MB), {gb_size} (GB).")

def render_markdown_to_html(markdown_text):
    # Convert markdown to HTML
    html_text = markdown.markdown(markdown_text)
  
  
    content_div = f"""
    <div class="container" >
        {html_text}
    </div>
    """

    
    print("HTML file created: html")

    return html_text

class Jedit:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_json()  # Automatically load JSON data

    def load_json(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"JSON file not found at {self.file_path}. Creating a new one.")
            return {}

    def add_key(self, key, value):
        self.data[key] = value
        self.save_json()
        print(f"Key '{key}' added to the site JSON file")

    def edit_key(self, key, new_value):
        if key in self.data:
            self.data[key] = new_value
            self.save_json()
            print(f"Key '{key}' updated with new value '{new_value}'")
        else:
            print(f"Key '{key}' does not exist in the JSON file")

    def save_json(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)
        print(f"JSON data saved to {self.file_path}")

    def find_key(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return False

    def delete_all(self):
        self.data = {}
        self.save_json()
        print(f"All keys have been deleted from the JSON file")

class JObject:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __getattr__(self, name):
        return self.__dict__.get(name, None)

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return str(self.__dict__)

class tprint:
    def __init__(self, message="Elapsed time:"):
        self.message = message
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._print_time)
        self.thread.daemon = True
        self.start()

    def start(self):
        self.start_time = time.time()
        self.thread.start()

    def stop(self):
        self._stop_event.set()
        self.thread.join()

    def _print_time(self):
        while not self._stop_event.is_set():
            elapsed_time = time.time() - self.start_time
            print(f"\r{self.message} {elapsed_time:.2f} seconds", end='', flush=True)
            time.sleep(0.01)

import sqlite3
import json

class Table:
    def __init__(self, conn, tablename):
        self.conn = conn
        self.tablename = tablename
        self._create_table()

    def _create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS "{self.tablename}" (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        """
        self._execute_query(query)

    def _execute_query(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

    def set(self, key, value):
        value = json.dumps(value)
        query = f"""
        INSERT INTO "{self.tablename}" (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value;
        """
        self._execute_query(query, (key, value))

    def get(self, key):
        query = f"SELECT value FROM \"{self.tablename}\" WHERE key = ?;"
        cursor = self._execute_query(query, (key,))
        result = cursor.fetchone()
        if result:
            return json.loads(result[0])
        return None

    def exists(self, key):
        query = f"SELECT 1 FROM \"{self.tablename}\" WHERE key = ? LIMIT 1;"
        cursor = self._execute_query(query, (key,))
        return cursor.fetchone() is not None

    def delete_table(self):
        query = f"DROP TABLE IF EXISTS \"{self.tablename}\";"
        self._execute_query(query)

    def get_keys(self):
        query = f"SELECT key FROM \"{self.tablename}\";"
        cursor = self._execute_query(query)
        keys = [row[0] for row in cursor.fetchall()]
        return keys

class QuickDB:
    def __init__(self, filename='example.db'):
        self.filename = filename
        self.conn = sqlite3.connect(filename)
        self._initialize_tables()

    def create_table(self, tablename):
        table = Table(self.conn, tablename)
        setattr(self, tablename, table)
        return table

    def _initialize_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        cursor = self.conn.cursor()
        cursor.execute(query)
        tables = cursor.fetchall()
        for table in tables:
            tablename = table[0]
            self.create_table(tablename)

    def list_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        cursor = self.conn.cursor()
        cursor.execute(query)
        tables = [row[0] for row in cursor.fetchall()]
        return tables

def speak_text(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Optional: Set properties like voice and speech rate
    engine.setProperty('rate', 250)  # Speed percent (can go above 100)
    engine.setProperty('volume', 0.2)  # Volume 0-1

    # Adding text to the speaking queue
    engine.say(text)

    # Blocks while processing all the commands in the queue
    engine.runAndWait()


def create_directory_structure(directory, ignore_list):
    result = []
    files_list = []

    # Walk through directory tree, ignoring specified files and directories
    for root, dirs, files in os.walk(directory):
        # Filter directories to ignore
        dirs[:] = [d for d in dirs if not any(ignored in os.path.join(root, d) for ignored in ignore_list)]
        for file in files:
            file_path = os.path.join(root, file)
            if not any(ignored in file_path for ignored in ignore_list):
                files_list.append(file_path)
    
    relative_files = [os.path.relpath(file, directory) for file in files_list]
    relative_files.sort()
    
    print('Generating directory structure...')
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
    
    return result, files_list

def write_directory_structure(filename, directory_structure):
    instructions = (
        "Only show files you edit.\n"
        "This is the current version of the project directory and its file contents.\n\n"
    )
    heading = "Directory Structure of the Project\n"
    heading += "This file contains a structured listing of all directories and files within the project. Contents are included for specified files.\n\n"

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(instructions)
        file.write(heading)
        file.write('\n'.join(directory_structure) + "\n\n")

def append_file_contents(filename, files_list):
    with open(filename, 'a', encoding='utf-8') as file:
        for file_path in files_list:
            relative_path = os.path.relpath(file_path, os.path.dirname(os.path.abspath(__file__)))
            file.write(f"Contents of {relative_path}:\n")
            file.write("--- start -----------------------\n\n")
            try:
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.mp3', '.wav', '.flac', '.aac', '.ogg')):
                    file.write(f"{relative_path} is an image or audio file.\n")
                else:
                    with open(file_path, 'r', encoding='utf-8') as content_file:
                        file.write(content_file.read())
            except Exception as e:
                file.write(f"Error reading file: {str(e)}")
            file.write("\n\n--- end -----------------------\n\n\n")









import webview
from webview.dom import ManipulationMode
import threading
import openai
import markdown2
from dotenv import load_dotenv
import os
import json
import html  # For escaping HTML characters
from function import speak_text
from html import escape
import markdown
from time import sleep
import function as fun
load_dotenv()


def convert_markdown_to_html(md_filepath, html_filepath):

    with open(md_filepath, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()
    
    html_content = markdown2.markdown(md_content, extras=["fenced-code-blocks", "code-friendly", "highlightjs-lang"])
    
    styled_html_content = f"""
    <div>
 
        {html_content}
    </div>
    """
   
    # Save the styled HTML content to a new file
    with open(html_filepath, 'w', encoding='utf-8') as html_file:
        html_file.write(styled_html_content)
    return styled_html_content

def append_response(html_content):


   # Append the HTML content to the body
    window.evaluate_js(f"""
    var newElement = document.createElement('div');
    newElement.innerHTML = `{html_content}`;
    var mom = document.getElementById('chatbox');
    mom.appendChild(newElement);
    """)

def save_to_textfile(filename, content):
    """Saves the provided content to a text file."""
    with open(filename, 'w') as file:
        file.write(content)


def Ask_ai(message):
    
    print(f"Debug: Starting stream for message: {message}")
    
    client = openai.OpenAI(api_key=os.getenv('OPENAIKEY'))
    messages = [
            {"role": "system", "content": 'you are a helpful assistant. answer any questions, respond using markdown.'},
            {"role": "user", "content": message}
        ]
        
    #speak_text('waiting for response')
    tp= fun.tprint('WAITING FOR RESPONSE')
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    print('RESPONSE RECIEVED.')
    tp.stop()
    return response.choices[0].message.content

 

def format_response(response):

   
    thefilename='response.txt'
    html_file_path ='response.html'
    save_to_textfile(thefilename,response)
    thehtml = convert_markdown_to_html(thefilename, html_file_path)
    append_response(thehtml)


def loadresponse(message):
    response=Ask_ai(message)
    format_response(response)


def setup_chat_ui():

    container = window.dom.get_element('#container')
    chatbox = window.dom.get_element('#chatbox')
    user_input = window.dom.get_element('#userInput')
    send_button = window.dom.get_element('#sendButton')


    def on_send_click(event):
        #user_input.value = 'Write a sample python script'
        message = user_input.value

        if message:
            user_message = window.dom.create_element(f'<div class="msg">{message}</div>', parent=chatbox)
            user_message.style['border'] = '0px solid black'
            user_message.style['padding'] = '20px'
            user_message.style['margin-bottom']='20px'
            user_input.value = '' 

            threading.Thread(target=loadresponse, args=(message, ), daemon=True).start()
   
    send_button.on('click', on_send_click)


def config_btn1():
    button1 = window.dom.get_element('#btn1')
    def clickfun(event):
        message='button click'
        user_message = window.dom.create_element(f'<div class="msg">{message}</div>', parent='#chatbox')
        user_message.style['border'] = '0px solid black'
        user_message.style['padding'] = '20px'
        user_message.style['margin-bottom']='20px'

   
    button1.on('click', clickfun)


def add_element(mom, t):
    count = 0
    element = window.dom.create_element('<div>Newly added element 11</div>', parent=mom)
    element.style['width'] = '200px'
    element.style['border'] = '1px solid black'
    element.style['padding'] = '10px'
    element.text = t
    print('element added')

    def onclick(event):
        nonlocal count  # Use nonlocal to modify the count variable
        print('clicked')
        count += 1
        element.text = t + ' count ' + str(count)

    element.on('click', onclick)
    element.events.click = onclick

def ui_manager(s):
    print(s)
    setup_chat_ui()
    config_btn1()

def load_html():
    # Replace 'index.html' with the path to your HTML file
    with open('index.html', 'r') as file:
        html = file.read()
    return html




class Api:
    def __init__(self):
        pass

    def list_directory(self, directory):
        print(directory)
        if os.path.isdir(directory):
            files_and_folders = os.listdir(directory)
            print(f"Contents of {directory}:")
            for item in files_and_folders:
                print(item)
            return files_and_folders
        else:
            return "The provided path is not a directory."

    def open_file_dialog(self):
        file_types = ('Image Files (*.bmp;*.jpg;*.gif)', 'All files (*.*)')

        result = window.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=True #, file_types=file_types
        )
        print(result[0])
        directory_path = os.path.dirname(result[0])
        print(directory_path)
        fun.make_program_prompt(directory_path)
        return result


if __name__ == "__main__":

    global window
    api=Api()
    window = webview.create_window('PyWebView - Dynamic UI Setup',html=load_html(), js_api=api)
    thread = threading.Thread(target=ui_manager, args=('start',), daemon=True)
    thread.start()

    webview.start(debug=False)
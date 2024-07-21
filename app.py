import os
import base64
import threading
import tkinter as tk
import random
import string
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image, ImageTk
from openai import OpenAI
from tkinter import ttk, scrolledtext
from screeninfo import get_monitors
import traceback
import mss
import mss.tools
from files.lib import *

load_dotenv()
api_key = os.getenv('OPENAIKEY')

Path('files/images').mkdir(parents=True, exist_ok=True)
Path('files/responses').mkdir(parents=True, exist_ok=True)
temp_image_path = 'files/images/temp_img.jpg'

request_in_progress = threading.Event()

def generate_random_filename(prefix):
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    return f"{prefix}_{random_str}.txt"

def take_screenshot(monitor_number):
    monitors = get_monitors()
    if monitor_number < 1 or monitor_number > len(monitors):
        raise ValueError("Invalid monitor number")
    monitor = monitors[monitor_number - 1]
    with mss.mss() as sct:
        monitor_rect = {
            'top': monitor.y,
            'left': monitor.x,
            'width': monitor.width,
            'height': monitor.height
        }
        screenshot = sct.grab(monitor_rect)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=temp_image_path)
    update_image_preview(temp_image_path)

def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_stream(encoded_image, system_prompt, user_question):
    client = OpenAI(api_key=api_key)
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': [
            {'type': 'text', 'text': user_question},
            {'type': 'image_url', 'image_url': {'url': f'data:image/jpg;base64,{encoded_image}'}}
        ]}
    ]
    stream = client.chat.completions.create(model='gpt-4o', messages=messages, stream=True)
    full_response = ''
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            full_response += chunk.choices[0].delta.content
            response_text_area.insert(tk.END, chunk.choices[0].delta.content)
            response_text_area.see(tk.END)
    return full_response

def save_response_to_file(filename, response):
    with open(filename, 'w') as file:
        file.write(response)

def get_last_line(text_widget):
    return text_widget.get('end-2l', 'end-1c').strip()

def on_return_key(event):
    if request_in_progress.is_set():
        return 'break'
    user_input = get_last_line(response_text_area)
    if user_input.startswith('//'):
        user_question = user_input[2:].strip()
        if user_question:
            response_text_area.insert(tk.END, '\n')
            threading.Thread(target=submit_request, args=(user_question,), daemon=True).start()
        return 'break'
    elif user_input.startswith('/system'):
        system_msg = user_input[7:].strip()
        response_text_area.insert(tk.END, '\n')
        show_system_message(system_msg)
        return 'break'
    return 'continue'

def submit_request(user_question):
    request_in_progress.set()
    monitor_number = selected_monitor.get()
    system_prompt = system_message

    try:
        take_screenshot(monitor_number)
        encoded_image = encode_image(temp_image_path)
        response = analyze_image_stream(encoded_image, system_prompt, user_question)
        save_response_to_file('files/responses/' + generate_random_filename('response'), response)
        insert_response_with_button(response)
        refresh_file_list()
    except Exception as e:
        response_text_area.insert(tk.END, '\n' + str(e) + '\n' + traceback.format_exc() + '\n')
        response_text_area.see(tk.END)
    finally:
        request_in_progress.clear()

def show_system_message(system_msg):
    global system_message
    system_message = system_msg
    response_text_area.insert(tk.END, system_msg + '\n\n')
    save_button = tk.Button(response_text_area, text='Save System Msg', height=1, width=15, command=lambda: save_system_msg(response_text_area.get('1.0', tk.END).strip()))
    response_text_area.window_create(tk.END, window=save_button)
    response_text_area.insert(tk.END, '\n\n')

def save_system_msg(current_msg):
    global system_message
    if system_message != current_msg:
        system_message = current_msg
        save_response_to_file('files/responses/' + generate_random_filename('system_message'), system_message)
        refresh_file_list()

def save_and_disable_button(response, button):
    save_response_to_file('files/responses/' + generate_random_filename('response'), response)
    button.config(state=tk.DISABLED)
    refresh_file_list()

def insert_response_with_button(response):
    response_text_area.insert(tk.END, '\n\n')
    save_button = tk.Button(response_text_area, text='Save', height=1, width=5, command=lambda: save_and_disable_button(response, save_button))
    response_text_area.window_create(tk.END, window=save_button)
    response_text_area.insert(tk.END, '\n\n' + response + '\n')
    response_text_area.see(tk.END)

def update_image_preview(image_path):
    img = Image.open(image_path)
    img.thumbnail((200, 150))
    img = ImageTk.PhotoImage(img)
    image_preview_label.config(image=img)
    image_preview_label.image = img

def select_monitor(monitor_number):
    selected_monitor.set(monitor_number)
    for button in monitor_buttons:
        button.config(bg='SystemButtonFace')
    monitor_buttons[monitor_number - 1].config(bg='green')
    take_screenshot(monitor_number)

def refresh_file_list():
    for widget in file_list_frame.winfo_children():
        widget.destroy()
    for filename in os.listdir('files/responses'):
        file_path = os.path.join('files/responses', filename)
        file_button = tk.Button(file_list_frame, text=filename, command=lambda f=file_path: load_file_content(f))
        file_button.pack(fill=tk.X, padx=10, pady=2)
        del_button = tk.Button(file_list_frame, text='Delete', command=lambda f=file_path: delete_file(f))
        del_button.pack(fill=tk.X, padx=10, pady=2)

def load_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    response_text_area.delete('1.0', tk.END)
    response_text_area.insert(tk.END, content)
    response_text_area.see(tk.END)

def delete_file(file_path):
    os.remove(file_path)
    refresh_file_list()

system_message = 'You are a helpful assistant who analyzes images and responds in markdown to any question.'
default_user_message = '//What is this image about?'

root = tk.Tk()
root.title('Screenshot Capture')
root.geometry('1200x800')

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

select_monitor_frame = ttk.LabelFrame(left_frame, text='Select Monitor and Image Preview')
select_monitor_frame.pack(pady=5, fill=tk.X)

monitor_buttons_frame = tk.Frame(select_monitor_frame)
monitor_buttons_frame.pack(pady=5, fill=tk.X)
selected_monitor = tk.IntVar(value=1)
monitor_buttons = [tk.Button(monitor_buttons_frame, text=f'Monitor {idx+1}', command=lambda idx=idx: select_monitor(idx+1)) for idx, _ in enumerate(get_monitors())]
for btn in monitor_buttons:
    btn.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X)
monitor_buttons[0].config(bg='green')

image_preview_label = tk.Label(select_monitor_frame)
image_preview_label.pack(pady=5)

response_frame = ttk.LabelFrame(right_frame, text='Response')
response_frame.pack(pady=5, fill=tk.BOTH, expand=True)

response_text_area = scrolledtext.ScrolledText(response_frame, height=30, width=150, wrap=tk.WORD)
response_text_area.pack(pady=5, fill=tk.BOTH, expand=True)
response_text_area.insert(tk.END, system_message + '\n\n\n\n' + default_user_message)
response_text_area.see(tk.END)
response_text_area.bind('<Return>', on_return_key)

file_list_frame = ttk.LabelFrame(left_frame, text='Responses')
file_list_frame.pack(pady=10, fill=tk.BOTH, expand=True)

refresh_file_list()
select_monitor(1)

root.mainloop()

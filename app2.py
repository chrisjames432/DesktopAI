import os
from PIL import Image, ImageTk
from dotenv import load_dotenv
import base64
from openai import OpenAI
from pathlib import Path
import tkinter as tk
from tkinter import ttk, scrolledtext
from screeninfo import get_monitors
import traceback
import uuid
import mss
import mss.tools
import threading
from files.lib import *

load_dotenv()
api_key = os.getenv('OPENAIKEY')
Path('files/images').mkdir(parents=True, exist_ok=True)
Path('files/responses').mkdir(parents=True, exist_ok=True)
temp_image_path = 'files/images/temp_img.jpg'
response_file_path = 'files/responses.txt'

request_in_progress = threading.Event()

def take_screenshot(monitor_number):
    monitors = get_monitors()
    if monitor_number < 1 or monitor_number > len(monitors):
        raise ValueError("Invalid monitor number")
    monitor = monitors[monitor_number - 1]
    with mss.mss() as sct:
        monitor_rect = {
            "top": monitor.y,
            "left": monitor.x,
            "width": monitor.width,
            "height": monitor.height
        }
        screenshot = sct.grab(monitor_rect)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=temp_image_path)
    update_image_preview(temp_image_path)
    return temp_image_path

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_stream(encoded_image, system_prompt, user_question):
    client = OpenAI(api_key=api_key)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": [
            {"type": "text", "text": user_question},
            {"type": "image_url", "image_url": {"url": f"data:image/jpg;base64,{encoded_image}"}}
        ]}
    ]

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True
    )

    buffer = ""
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            buffer += chunk.choices[0].delta.content
            full_response += chunk.choices[0].delta.content
            response_text_area.insert(tk.END, chunk.choices[0].delta.content)
            response_text_area.update()
            buffer = ""
    return full_response

def generate_random_filename(prefix):
    return f"{prefix}_{uuid.uuid4()}.txt"

def save_response_to_file(filename, response):
    with open(filename, 'w') as file:
        file.write(response)

def get_last_line(text_widget):
    last_line_index = text_widget.index("end-1c linestart")
    return text_widget.get(last_line_index, tk.END).strip()

def on_return_key(event):
    if request_in_progress.is_set():
        return "break"
    user_input = get_last_line(response_text_area)
    if user_input.startswith("//"):
        user_question = user_input[2:].strip()
        if user_question:
            response_text_area.delete("1.0", tk.END)
            threading.Thread(target=submit_request, args=(user_question,), daemon=True).start()
    elif user_input.startswith("/system"):
        system_msg = user_input[7:].strip()
        response_text_area.delete("1.0", tk.END)
        show_system_message(system_msg)
    return "break"

def submit_request(user_question):
    request_in_progress.set()
    monitor_number = selected_monitor.get()
    system_prompt = system_message if system_message else "You are a helpful assistant who analyzes images and responds in markdown to any question."

    try:
        image_path = take_screenshot(monitor_number)
        encoded_image = encode_image(image_path)
        response_text_area.delete("1.0", tk.END)
        response = analyze_image_stream(encoded_image, system_prompt, user_question)
        with open(response_file_path, 'a') as file:
            file.write(response + '\n\n')
        insert_response_with_button(response)
    except Exception as e:
        error_message = f"{str(e)}\n{traceback.format_exc()}"
        response_text_area.delete("1.0", tk.END)
        print_progress(f"Error: {error_message}")
    finally:
        request_in_progress.clear()

def show_system_message(system_msg):
    global system_message
    system_message = system_msg
    response_text_area.insert(tk.END, system_msg + '\n\n')
    button = tk.Button(response_text_area, text="Save System Msg", height=1, width=15, 
                       command=lambda: save_system_msg(response_text_area.get("1.0", tk.END).strip()))
    response_text_tags = response_text_area.index(tk.END)
    response_text_area.window_create(response_text_tags, window=button)
    response_text_area.insert(tk.END, '\n\n')

def save_system_msg(current_msg):
    global system_message
    if system_message != current_msg:
        system_message = current_msg
        fn = 'files/responses/' + generate_random_filename("system_message")
        save_response_to_file(fn, system_message)

def save_and_disable_button(response, button):
    fn = 'files/responses/' + generate_random_filename("myfile")
    save_response_to_file(fn, response)
    button.config(state=tk.DISABLED)

def insert_response_with_button(response):
    response_text_area.insert(tk.END, response + '\n\n')
    button = tk.Button(response_text_area, text="Save", height=1, width=5, 
                       command=lambda: save_and_disable_button(response, button))
    response_text_tags = response_text_area.index(tk.END)
    response_text_area.window_create(response_text_tags, window=button)
    response_text_area.insert(tk.END, '\n\n')

def print_progress(message):
    response_text_area.insert(tk.END, '\n' + message + "\n")
    response_text_area.see(tk.END)
    response_text_area.update()
    print(message)

def update_image_preview(image_path):
    img = Image.open(image_path)
    img.thumbnail((200, 150))
    img = ImageTk.PhotoImage(img)
    image_preview_label.config(image=img)
    image_preview_label.image = img

def select_monitor(monitor_number):
    global selected_monitor
    selected_monitor.set(monitor_number)
    for button in monitor_buttons:
        button.config(bg="SystemButtonFace")
    monitor_buttons[monitor_number - 1].config(bg="green")
    take_screenshot(monitor_number)

system_message = "You are a helpful assistant who analyzes images and responds in markdown to any question."
default_user_message = "//What is this image about?"

root = tk.Tk()
root.title("Screenshot Capture")
root.geometry("1200x800")

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

select_monitor_frame = ttk.LabelFrame(left_frame, text="Select Monitor and Image Preview")
select_monitor_frame.pack(pady=5, fill=tk.X)

monitor_buttons_frame = tk.Frame(select_monitor_frame)
monitor_buttons_frame.pack(pady=5, fill=tk.X)
selected_monitor = tk.IntVar(value=1)
monitor_buttons = []

for idx, monitor in enumerate(get_monitors(), start=1):
    btn = tk.Button(monitor_buttons_frame, text=f"Monitor {idx}", command=lambda idx=idx: select_monitor(idx))
    if idx == 1:
        btn.config(bg="green")
    btn.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X)
    monitor_buttons.append(btn)

image_preview_label = tk.Label(select_monitor_frame)
image_preview_label.pack(pady=5)

response_text_label = tk.Label(right_frame, text="Response:")
response_text_label.pack(pady=5)
response_text_area = scrolledtext.ScrolledText(right_frame, height=30, width=150)
response_text_area.pack(pady=5, fill=tk.BOTH, expand=True)

response_text_area.insert(tk.END, system_message + '\n\n\n\n' + default_user_message)

response_text_area.bind("<Return>", on_return_key)

select_monitor(1)
root.mainloop()

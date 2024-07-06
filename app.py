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
from files.lib import *

load_dotenv()
api_key = os.getenv('OPENAIKEY')
Path('files/images').mkdir(parents=True, exist_ok=True)
Path('files/responses').mkdir(parents=True, exist_ok=True)
temp_image_path = 'files/images/temp_img.jpg'
response_file_path = 'files/responses.txt'

def take_screenshot(monitor_number):
    print_progress("Taking screenshot...")
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
    print_progress("Encoding image...")
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

def on_submit():
    monitor_number = selected_monitor.get()
    system_prompt = system_prompt_entry.get("1.0", tk.END).strip()
    user_question = user_question_entry.get("1.0", tk.END).strip()

    try:
        image_path = take_screenshot(monitor_number)
        encoded_image = encode_image(image_path)
        response_text_area.delete("1.0", tk.END)
        response = analyze_image_stream(encoded_image, system_prompt, user_question)
        print(response)
        with open(response_file_path, 'a') as file:
            file.write(response + '\n\n')

        insert_response_with_button(response)
    except Exception as e:
        error_message = f"{str(e)}\n{traceback.format_exc()}"
        response_text_area.delete("1.0", tk.END)
        print_progress(f"Error: {error_message}")

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

system_prompt_label = tk.Label(left_frame, text="System Prompt:")
system_prompt_label.pack(pady=5)
system_prompt_entry = tk.Text(left_frame, height=5, width=50)
system_prompt_entry.pack(pady=5)
system_prompt_entry.insert(tk.END, 'You are a helpful assistant who analyzes images and responds in markdown to any question.')

user_question_label = tk.Label(left_frame, text="User Question:")
user_question_label.pack(pady=5)
user_question_entry = tk.Text(left_frame, height=5, width=50)
user_question_entry.pack(pady=5)
user_question_entry.insert(tk.END, 'What is this image about? Can you summarize it?')

submit_button = tk.Button(left_frame, text="Submit", command=on_submit)
submit_button.pack(pady=20)

response_text_label = tk.Label(right_frame, text="Response:")
response_text_label.pack(pady=5)
response_text_area = scrolledtext.ScrolledText(right_frame, height=30, width=150)
response_text_area.pack(pady=5, fill=tk.BOTH, expand=True)

select_monitor(1)
root.mainloop()

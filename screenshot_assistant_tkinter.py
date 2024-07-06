import os
from PIL import ImageGrab
from dotenv import load_dotenv
import base64
from openai import OpenAI
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from function import *

# Load environment variables from .env file
load_dotenv()

# Fetch the OpenAI API key from the .env file
api_key = os.getenv('OPENAIKEY')

# Ensure the "images" folder exists
Path('images').mkdir(exist_ok=True)
temp_image_path = 'images/temp_img.jpg'

# Function to take a screenshot, resize it, and save it
def take_screenshot(x1, y1, x2, y2):
    print('Screenshot captured')
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    screenshot = screenshot.resize((1920, 1080))
    screenshot.save(temp_image_path, 'JPEG')
    return temp_image_path

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to analyze the image using GPT-4.0
def analyze_image(encoded_image, system_prompt, user_question):
    client = OpenAI(api_key=api_key)

    print('GEN RESPONSE')
    tp = tprint('start')

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": user_question},
                {"type": "image_url", "image_url": {"url": f"data:image/jpg;base64,{encoded_image}"}}
            ]}
        ]
    )
    tp.stop()
    response = response.choices[0].message.content
    return response

# Function to handle the submit action
def on_submit(system_prompt, user_question, x1, y1, x2, y2):
    image_path = take_screenshot(x1, y1, x2, y2)
    encoded_image = encode_image(image_path)
    response = analyze_image(encoded_image, system_prompt, user_question)
    save_response_to_file('capture_response.txt',response)
    print('')
    print(response)
    messagebox.showinfo("Assistant Response", response)

# Function to start the screenshot capture
def start_capture():
    global root
    global start_x, start_y, end_x, end_y

    start_x = root.winfo_x()
    start_y = root.winfo_y()
    end_x = start_x + root.winfo_width()
    end_y = start_y + root.winfo_height()
    
    on_submit(system_prompt, user_question, start_x, start_y, end_x, end_y)

# Create the Tkinter window
root = tk.Tk()
root.title("Screenshot Capture")
root.geometry("400x400")
root.attributes('-alpha', 0.3)
root.attributes('-topmost', True)

start_x = 0
start_y = 0
end_x = 0
end_y = 0

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=start_capture)
submit_button.pack(side=tk.BOTTOM, pady=20)

# Variables for the assistant
system_prompt = 'You are a helpful assistant who analyzes images and responds in markdown to any question.'
user_question = 'write the code for me.'

# Main loop
root.mainloop()

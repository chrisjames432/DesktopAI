import os
from PIL import ImageGrab
from dotenv import load_dotenv
import base64
from openai import OpenAI
from pathlib import Path
import io
import soundfile as sf
import sounddevice as sd
import webview
import threading
import time
import tkinter as tk
from tkinter import filedialog
from function import *

# Load environment variables from .env file
load_dotenv()

# Fetch the OpenAI API key from the .env file
api_key = os.getenv('OPENAIKEY')

# Ensure the "images" folder exists
Path('images').mkdir(exist_ok=True)

temp_image_path = 'images/temp_img.jpg'

# Function to take a screenshot, resize it, and save it
def take_screenshot():
    print('Screenshot captured')
    screenshot = ImageGrab.grab()
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

    return response

# Function to convert text to speech and play it using buffer
def text_to_speech(text, voice="fable", speed=1.0):
    client = OpenAI(api_key=api_key)
    
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        response_format="opus",
        input=text,
        speed=speed
    )

    buffer = io.BytesIO()
    for chunk in response.iter_bytes(chunk_size=4096):
        buffer.write(chunk)
    buffer.seek(0)

    with sf.SoundFile(buffer, 'r') as sound_file:
        data = sound_file.read(dtype='int16')
        sd.play(data, sound_file.samplerate)
        sd.wait()

# Function to handle the submit action
def on_submit(system_prompt, user_question):
    image_path = take_screenshot()
    encoded_image = encode_image(image_path)
    response = analyze_image(encoded_image, system_prompt, user_question)
    assistant_message = response.choices[0].message.content
    tthread = threading.Thread(target=text_to_speech, args=(assistant_message,), daemon=True)
    tthread.start()
    
    return assistant_message

class Api:

    def submit_form(self, system_prompt, user_question):
        return on_submit(system_prompt, user_question)

    def pick_directory(self):
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        directory = filedialog.askdirectory()
        root.destroy()
        return directory
    

    

def update_counter(window):
    start_time = time.time()
    while True:
        elapsed_time = int(time.time() - start_time)
        window.evaluate_js(f'updateCounter({elapsed_time})')
        time.sleep(1)

if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'Image Analysis with GPT-4',
        'index.html',
        js_api=api,
        width=1600,
        height=800,
        resizable=True  # Make the window fixed-size
    )

    counter_thread = threading.Thread(target=update_counter, args=(window,), daemon=True)
    counter_thread.start()

    webview.start()

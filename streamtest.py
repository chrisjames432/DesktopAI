
import time
from openai import OpenAI

def generate_stream_response(system_msg, user_msg, optimal_buffer_size=80, delay=0.005, fast_delay=0.0001):
    # Initialize the OpenAI client
    client = OpenAI(api_key='')

    # Create messages for the system and user
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg}
    ]

    # Generate the response
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

            # Check if the buffer length exceeds the optimal buffer size
            if len(buffer) >= optimal_buffer_size:
                for char in buffer:
                    print(char, end="", flush=True)
                    time.sleep(delay)
                buffer = ""

    # Print any remaining characters in the buffer faster
    for char in buffer:
        print(char, end="", flush=True)
        time.sleep(fast_delay)

    return full_response


def streamres(sys, usr, filename='output.txt'):
    client = OpenAI(api_key='')

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": usr}
        ],
        stream=True
    )

    with open(filename, 'a') as file:
        for chunk in completion:
            data = chunk.choices[0].delta
            print(data)
            file.write(str(data) + '\n')






usr= 'write a short descriptin of a cat in a python scritp'
system='you are a helpful assistant. answer any questions, respond in markdown'
response = streamres(system,usr)
print(response.content)
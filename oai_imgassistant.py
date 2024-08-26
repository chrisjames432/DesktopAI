import base64
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAIKEY')

def analyze_image_stream(encoded_image, system_prompt, user_question):
    client = OpenAI(api_key=api_key)
    stream = client.chat.completions.create(model='gpt-4o', messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': [
            {'type': 'text', 'text': user_question},
            {'type': 'image_url', 'image_url': {'url': f'data:image/jpg;base64,{encoded_image}'}}
        ]}
    ], stream=True)

    full_response = ''
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end='')
            full_response += chunk.choices[0].delta.content

    return full_response

def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def main():
    image_path = input("Enter the path to the image file: ")
    encoded_image = encode_image(image_path)
    system_prompt = "You are a helpful assistant analyzing an image."
    user_question = "What is this image about?"
    
    print("Analyzing the image...")
    analyze_image_stream(encoded_image, system_prompt, user_question)

if __name__ == "__main__":
    main()

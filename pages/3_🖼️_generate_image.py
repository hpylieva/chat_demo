import requests
from io import BytesIO

import streamlit as st
from openai import OpenAI
from PIL import Image

from utils import configure_openai_api_key, check_password_routine

# Check password before proceeding
check_password_routine()

# Configure the OpenAI API key
configure_openai_api_key()

# Create an OpenAI client instance
client = OpenAI()

# Define constants for style prompts
STYLE_PROMPTS = [
    'Photorealistic', 'Advertising', 'Cubist', 'Cyberpunk', 'Pop art', 'Street art', 'Monet'
]

def generate_image(prompt: str, size: str, quality: str) -> Image.Image:
    """
    Generates an image based on the given prompt, size, and quality.

    Args:
        prompt (str): The prompt for image generation.
        size (str): The size of the generated image.
        quality (str): The quality of the generated image.

    Returns:
        Image.Image: The generated image.
    """
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality=quality,
        n=1,
    )
    image_url = response.data[0].url
    response = requests.get(image_url)
    return Image.open(BytesIO(response.content))

# Streamlit UI
st.title("Image Generation")

user_query = st.text_input(
    label='Write your request to generate image:',
    value='Dog pilot in orange costume'
)

st.write('Select style of your image')
columns = st.columns(len(STYLE_PROMPTS))

for col, style_name in zip(columns, STYLE_PROMPTS):
    if col.button(style_name):
        st.session_state['selected_style'] = style_name

st.session_state['image_size'] = st.selectbox("Choose size of the image", ['1024x1024', '1792x1024', '1024x1792'])
st.session_state['image_quality'] = st.selectbox("Choose quality of the image", ['standard', 'hd'])

if 'selected_style' in st.session_state:
    final_prompt = user_query + f" in {st.session_state['selected_style']} style."
    st.write(f'**Your prompt: "{final_prompt}**"')

if 'selected_style' in st.session_state and st.button('GENERATE!'):
    with st.spinner('Wait for it...'):
        img = generate_image(final_prompt, st.session_state['image_size'], st.session_state['image_quality'])
        st.image(img)

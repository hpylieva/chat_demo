from openai import OpenAI
import streamlit as st
import utils
from PIL import Image
import requests
from io import BytesIO
from utils import check_password_routine

check_password_routine()

utils.configure_openai_api_key()
client = OpenAI()

PROMPTS = {
    'Peaceful morning': 'Peaceful morning',
    'Logo for a blockchain startup': 'Logo for a blockchain startup',
    'Cubist Still Life': (
        'A cubist painting of a still life with geometric shapes, fragmented forms, '
        'and multiple perspectives, inspired by the works of Pablo Picasso and Georges Braque, '
        'using a muted color palette.'
    )
}

st.title("Image Generation")

user_query = st.text_input(label="Write your request to generate image:")

st.write('Or select from examples:')
st.session_state['selected_prompt'] = None
columns = st.columns(len(PROMPTS))

for col, (prompt_name, prompt_description) in zip(columns, PROMPTS.items()):
    if col.button(prompt_name):
        st.session_state['selected_prompt'] = prompt_description

final_prompt = user_query if user_query else st.session_state['selected_prompt']
st.write(f'Your prompt: "{final_prompt}"')


if final_prompt:
    response = client.images.generate(
        model="dall-e-3",
        prompt=final_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    st.image(img)
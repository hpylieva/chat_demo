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

STYLE_PROMPTS = [
    'Photorealistic', 'Advertising', 'Cubist', 'Cyberpunk', 'Pop art', 'Street art', 'Monet'
]

st.title("Image Generation")

user_query = st.text_input(
    label='Write your request to generate image:',
    value='Dog pilot in orange costume'
)

st.write('Select style of your image')
columns = st.columns(len(STYLE_PROMPTS))

for col, prompt_name in zip(columns, STYLE_PROMPTS):
    if col.button(prompt_name):
        st.session_state['selected_prompt'] = prompt_name
        st.write(prompt_name, st.session_state['selected_prompt'])

st.session_state['image_size'] = st.selectbox("Choose size of the image", ['1024x1024', '1792x1024', '1024x1792'])
st.session_state['image_quality'] = st.selectbox("Choose quality of the image", ['standard', 'hd'])

final_prompt = user_query + f" in {st.session_state['selected_prompt']} style."
st.write(f'**Your prompt: "{final_prompt}**"')

if st.button('GENERATE!'):
    st.spinner('Wait for it...')
    response = client.images.generate(
        model="dall-e-3",
        prompt=final_prompt,
        size=st.session_state['image_size'],
        quality=st.session_state['image_quality'],
        n=1,
    )
    image_url = response.data[0].url

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    st.image(img)
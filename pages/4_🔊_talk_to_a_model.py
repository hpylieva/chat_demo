from pathlib import Path
from typing import NoReturn

import openai
import streamlit as st
from streamlit_mic_recorder import mic_recorder, speech_to_text

from agents_setup import setup_internet_agent, get_agent_response
from utils import check_password_routine


check_password_routine()


def synthesize_speech(text_input: str, client: openai.OpenAI) -> NoReturn:
    """
    Converts the provided text input into spoken words in the form of an MP3 file.

    This function utilizes a text-to-speech service to generate speech from the given text.
    The resulting speech is saved as an MP3 file named 'speech.mp3' in the current working directory.

    Parameters:
    text_input (str): A string of text to be converted into speech.

    Returns:
    None: The function does not return a value but saves the speech output as 'speech.mp3'.
    """
    speech_file_path = "speech.mp3"
    response = client.audio.speech.create(
      model="tts-1",
      voice="alloy",
      input=text_input
    )
    response.stream_to_file(speech_file_path)

state = st.session_state
if 'text_received' not in state:
    state.text_received = []

c1, c2 = st.columns(2)
with c1:
    st.write("Ask something with your voice (English only):")
with c2:
    text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')

if text:
    state.text_received.append(text)

for text in state.text_received:
    st.write(f'Your question is: **{text}**')

    if st.button('Answer with voice!'):
        agent, client = setup_internet_agent()
        text_input = get_agent_response(agent, state.text_received)
        synthesize_speech(text_input, client)
        st.audio("speech.mp3")
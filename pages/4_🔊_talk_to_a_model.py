from pathlib import Path
import streamlit as st
from streamlit_mic_recorder import mic_recorder, speech_to_text
from agents_setup import setup_internet_agent, get_agent_response
from utils import check_password_routine

check_password_routine()

def synthesize_speech(text_input):
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

c1, c2= st.columns(2)
with c1:
    st.write("Convert speech to text:")
with c2:
    text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')

if text:
    state.text_received.append(text)

for text in state.text_received:
    st.text(text)

# st.write("Record your voice, and play the recorded audio:")
# recorded_audio=mic_recorder(start_prompt="⏺️", stop_prompt="⏹️", key='recorder')
#
# if recorded_audio:
#     st.ʼaudio(recorded_audio['bytes'])

if st.button('Answer with voice!'):
    agent, client = setup_internet_agent()
    text_input = get_agent_response(agent, state.text_received)
    synthesize_speech(text_input)
    st.audio("speech.mp3")

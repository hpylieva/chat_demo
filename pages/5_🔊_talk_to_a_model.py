from pathlib import Path
from st_audiorec import st_audiorec
from openai import OpenAI
import streamlit as st
from utils import check_password_routine

check_password_routine()

client = OpenAI()

# Title
st.title("Voice Recording and Transcription")

# Record audio
audio_data = st_audiorec()

if audio_data is not None:
    # Save the audio data to a file
    audio_file = Path("audio_file.wav")
    with open(audio_file, "wb") as f:
        f.write(audio_data)

    st.write("Audio recorded and saved as 'audio_file.wav'")

    # Button to send the request to the API
    if st.button("Transcribe Audio"):
        # API call (replace with your actual API client code)
        try:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            st.write("Transcription successful.")
            st.write(transcript)  # Display the transcription
        except Exception as e:
            st.error(f"An error occurred: {e}")
#
# response = client.audio.speech.create(
#   model="tts-1",
#   voice="alloy",
#   input="Today is a wonderful day to build something people love!"
# )
#
# response.stream_to_file(speech_file_path)
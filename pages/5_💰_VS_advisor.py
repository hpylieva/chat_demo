from openai import OpenAI
import streamlit as st
from utils import check_password_routine

check_password_routine()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.title("VC advisor")


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {'role': 'system', 'content': """
        You are a helpful friendly assistant, who answers on venture capitals questions. 
        Don't provide too much advices right away. Try to understand user's request first with questions."""}
    ]

for message in st.session_state.messages:
    if message["role"] != 'system':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        stream =  client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True
        )
        for response in stream:
            print(response)
            if response.choices[0].delta.content is not None:
                full_response += response.choices[0].delta.content
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
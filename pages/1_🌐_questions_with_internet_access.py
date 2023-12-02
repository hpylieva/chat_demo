import json
import os
import utils
import streamlit as st

from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler

from utils import check_password_routine

check_password_routine()

os.environ["SERPAPI_API_KEY"] = st.secrets['API_KEY']

st.set_page_config(page_title="ChatWeb", page_icon="🌐")
st.header('Chatbot with Internet Access')
st.write('Equipped with internet access, enables users to ask questions about recent events')

utils.configure_openai_api_key()
openai_model = "gpt-3.5-turbo"

def setup_agent():
    llm = ChatOpenAI(model_name=openai_model, streaming=True)
    tools = load_tools(["serpapi"], llm=llm)
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=True
    )
    return agent

PREPARED_PROMPTS = [
    'What was the last score in Dallas Cowboys game and when did it take place?',
    'Who won the oscar for the category Best Actor in 2023? In which movie they acted? What is IMDB rating of this movie?',
    'What was the latest Bitcoin price?'
]
user_query = st.text_input(label="Ask me anything!")

st.write('Or select a prepared text.')
st.session_state['selected_prompt'] = None
columns = st.columns(len(PREPARED_PROMPTS))

for col, prompt_name in zip(columns, PREPARED_PROMPTS):
    if col.button(prompt_name):
        st.session_state['selected_prompt'] = prompt_name

final_prompt = user_query if user_query else st.session_state['selected_prompt']

if final_prompt:
    st.write(f'Your prompt: "{final_prompt}"')
    agent = setup_agent()
    st_cb = StreamlitCallbackHandler(st.container())
    response = agent.run(final_prompt, callbacks=[st_cb])
    st.write(response)

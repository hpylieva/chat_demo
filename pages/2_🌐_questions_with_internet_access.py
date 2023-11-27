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

# creds = json.load(open('../chatgpt_creds.json'))
# openai.api_key = creds['OPENAI_API_KEY']
os.environ["SERPAPI_API_KEY"] = json.load(open('../search_creds.json'))['API_KEY']


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

user_query = st.text_input(label="Ask me anything!")
if user_query:
    agent = setup_agent()
    st_cb = StreamlitCallbackHandler(st.container())
    response = agent.run(user_query, callbacks=[st_cb])
    st.write(response)

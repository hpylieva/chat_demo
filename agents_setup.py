import os
import streamlit as st

from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, load_tools, AgentType
from langchain.callbacks import StreamlitCallbackHandler

import utils

# Set up OpenAI API key and model
utils.configure_openai_api_key()
openai_model = "gpt-3.5-turbo"


def setup_internet_agent():
    """Initializes and returns an internet agent along with the OpenAI client."""
    # Configure SERPAPI API key
    os.environ["SERPAPI_API_KEY"] = st.secrets['API_KEY']
    client = OpenAI()

    # Initialize ChatOpenAI with streaming
    llm = ChatOpenAI(model_name=openai_model, streaming=True)

    # Load necessary tools
    tools = load_tools(["serpapi"], llm=llm)

    # Initialize and return agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=True
    )
    return agent, client


def get_agent_response(agent, user_query):
    """Returns the agent's response to a user query."""
    st_cb = StreamlitCallbackHandler(st.container())
    response = agent.run(user_query, callbacks=[st_cb])
    return response

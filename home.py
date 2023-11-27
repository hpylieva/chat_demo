
import streamlit as st
from utils import check_password_routine

check_password_routine()

# Main Streamlit app starts here


st.set_page_config(
    page_title="Chatbots Demo",
    page_icon='💬',
    layout='wide'
)

st.header("Chatbots Demo")
st.write("""
Here you can find different examples of chatbot implementations catering to different use cases:

- **Context-Aware Chatbot**  
  This version of the chatbot is designed to remember and reference previous interactions within a session. 
  It provides responses that are contextually relevant to the ongoing conversation, 
  showcasing a more advanced and user-centric approach.

- **Chatbot with Internet Access**  
  Expanding the capabilities further, this chatbot can access the internet. 
  It's able to answer queries about recent events, fetch up-to-date information, 
  and incorporate real-time data into its responses, making it an ideal tool for current affairs and dynamic content.

- **Chat with Your Documents**  
  Tailored for specific information needs, this chatbot can access and retrieve information from custom documents. 
  This feature enables it to respond to queries based on the specific content of these documents, offering a highly 
  customized and information-rich user experience.

To explore sample usage of each chatbot, please navigate to the corresponding chatbot section.
""")
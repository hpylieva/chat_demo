import base64
import os
import utils
import streamlit as st
from streamlit_javascript import st_javascript
from streaming import StreamHandler

from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter

from utils import check_password_routine

def displayPDF(upl_file, ui_width):
    # Read file as bytes:
    bytes_data = upl_file.getvalue()

    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode("utf-8")

    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={str(ui_width)} height={str(ui_width*4/3)} type="application/pdf"></iframe>'

    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)

def display_pdf(pdf):

    # Display an image for the selected page
    image_bytes = pdf[page_number - 1].get_pixmap().tobytes()
    st.image(image_bytes, caption=f"Page {page_number} of {num_pages}")

check_password_routine()

st.set_page_config(page_title="ChatPDF", page_icon="📄")
st.header('Chat with your documents')
st.write('Has access to custom documents and can respond to user queries by referring to the content within those documents')
with st.expander("See explanation"):
    st.write("""
    Here we user an strategy called Retrieval-Augmented Generation (RAG) is used.

    RAG allows the LLM to present accurate information with source attribution. The output can include citations or 
    references to sources. Users can also look up source documents themselves if they require further clarification or 
    more detail. This can increase trust and confidence in your generative AI solution.

    Here is how it works in general:
    """)
    st.image("images/RAG_2.png")


class CustomDataChatbot:

    def __init__(self):
        utils.configure_openai_api_key()
        self.openai_model = "gpt-3.5-turbo"

    def save_file(self, file):
        folder = 'tmp'
        if not os.path.exists(folder):
            os.makedirs(folder)

        file_path = f'./{folder}/{file.name}'
        with open(file_path, 'wb') as f:
            f.write(file.getvalue())
        return file_path

    @st.spinner('Analyzing documents..')
    def setup_qa_chain(self, uploaded_files):
        # Load documents
        docs = []
        for file in uploaded_files:
            file_path = self.save_file(file)
            loader = PyPDFLoader(file_path)
            docs.extend(loader.load())

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)

        # Create embeddings and store in vectordb
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectordb = DocArrayInMemorySearch.from_documents(splits, embeddings)

        # Define retriever
        retriever = vectordb.as_retriever(
            search_type='mmr',
            search_kwargs={'k':2, 'fetch_k':4}
        )

        # Setup memory for contextual conversation
        memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True
        )

        # Setup LLM and QA chain
        llm = ChatOpenAI(model_name=self.openai_model, temperature=0, streaming=True)
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm, retriever=retriever, memory=memory, verbose=True)
        return qa_chain


    @utils.enable_chat_history
    def main(self):
        with st.sidebar:
            uploaded_files = st.sidebar.file_uploader(label='Upload PDF files', type=['pdf'], accept_multiple_files=True)
            if not uploaded_files:
                st.error("Please upload PDF documents to continue!")
                st.stop()


        if uploaded_files:

                user_query = st.chat_input(placeholder="Ask me anything about the doc!")
                # ui_width = st_javascript("window.innerWidth")
                # for file in uploaded_files:
                #     displayPDF(file, ui_width - 10)
                if uploaded_files and user_query:
                    qa_chain = self.setup_qa_chain(uploaded_files)

                    utils.display_msg(user_query, 'user')

                    with st.chat_message("assistant"):
                        st_cb = StreamHandler(st.empty())
                        response = qa_chain.run(user_query, callbacks=[st_cb])
                        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    st.session_state.messages = []
    obj = CustomDataChatbot()
    obj.main()
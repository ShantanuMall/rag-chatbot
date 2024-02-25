!pip install PyPDF2
!pip install langchain streamlit-chat


import streamlit as st
# from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS 
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from streamlit_chat import message
from langchain.llms import HuggingFaceHub

def extract_text_from_pdfs(pdfs):
    """
    This function will extract all the text from PDF files
    Input:
        pdfs: List of uploaded PDF files
    Returns:
        str: Concatenated text extracted from all PDF files
    """
    text = ""
    for pdf in pdfs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def split_text_into_chunks(text):
    """
    This function will split a long text into specified bits of chunks
    Input:
        text: The long text to be split
    Returns:
        list: List of text chunks
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1200,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def create_vector_store(text_chunks):
    """
    This function will create a vector database for storing embeddings
    Input:
        text_chunks: List of text chunks
    Returns:
        FAISS: Vector store for the text chunks
    """
    embeddings = OpenAIEmbeddings()
    # Some open source embeddings model using hugging face
    # embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    # embeddings = HuggingFaceInstructEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"
    # embeddings = HuggingFaceEmbeddings(model_name = 'Bmaidalun1020/bce-embedding-base_v1')
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store

def initialize_conversation_chain(vector_store):
    """
    This function will initialize a conversation chain for chat interaction using LLMs
    Input:
        vector_store: Vector store for text chunks using FAISS
    Returns:
        ConversationalRetrievalChain: Initialized conversation chain
    """
    chat_model = ChatOpenAI()
    # chat_model = HuggingFaceHub(repo_id="google/flan-t5-xxl",model_kwargs={"temperature":0.5,"max_length":512})
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=chat_model,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain

def process_user_input(user_question):
    """
    This function will process user input and generate a response 
    Input:
        user_question: User's question
    Returns:
        Nothing but displays User Questions and chatbot's answers
    """
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, chat in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            message(chat.content, is_user=True)
        else:
            message(chat.content)

def main():
    # load_dotenv()
    st.set_page_config(page_title='GST-bot', page_icon=':books:')

    if "conversation" not in st.session_state: #initializing session variables conversation and chat history
        st.session_state.conversation = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    #main UI
    st.header('Get Your GST Queries Resolved :books:')
    user_question = st.text_input('Ask your doubts')
    if user_question:
        process_user_input(user_question)

    with st.sidebar: # Sidebar UI
        st.subheader('GST-bot is here to solve your queries')
        st.write('Ask me questions related to the Goods and Services Tax in India')

        # Option to choose between uploading or using already uploaded documents
        st.subheader('\n')
        option = st.radio("Choose an option to proceed", ("Upload Documents", "Use Existing"))

        if option == "Upload Documents":
            uploaded_files = st.file_uploader('Please Upload PDFs', accept_multiple_files=True)
            if uploaded_files:
                pdf_docs = uploaded_files
        else:
            pdf_file_paths = [
                "pdfs_docs/gst_1.pdf",
                "pdfs_docs/gst_2.pdf",
                "pdfs_docs/gst_3.pdf"
            ]
            pdf_docs = [open(pdf_path, "rb") for pdf_path in pdf_file_paths]
        if st.button('Proceed'):
            with st.spinner('Processing Documents...'): #processing to be done after pdf documents uploaded by user
                #calling Extract text function from PDFs
                raw_text = extract_text_from_pdfs(pdf_docs)
                
                #calling Split text into manageable chunks function
                text_chunks = split_text_into_chunks(raw_text)

                #calling Create vector store for text chunks function
                vector_store = create_vector_store(text_chunks)

                #calling Initialize conversation chain function for chat interaction
                st.session_state.conversation = initialize_conversation_chain(vector_store)

if __name__ == '__main__':
    main()

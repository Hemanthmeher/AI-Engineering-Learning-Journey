import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

st.set_page_config(page_title="PDF Chatbot", layout="centered")

st.title("PDF Chatbot")

api_key = st.text_input("Enter Groq API Key", type="password")
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if api_key and uploaded_file:
    os.environ["GROQ_API_KEY"] = api_key

    temp_pdf_path = "temp.pdf"
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    @st.cache_resource
    def load_vectorstore(file_path):
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        return FAISS.from_documents(chunks, embeddings)

    vectorstore = load_vectorstore(temp_pdf_path)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    llm_model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_source_documents=True,
            output_key="answer"
        )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm_model,
        retriever=retriever,
        memory=st.session_state.memory
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_query := st.chat_input("Ask something about the PDF"):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        result = qa_chain({"question": user_query})
        answer = result["answer"]

        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API_KEY"

print("--- 1. Loading PDF and Building Vector Store ---")

pdf_path = "paper.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

print("--- 2. Setting up LLM and Memory ---")

llm_model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_source_documents=True,
    output_key="answer"
)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm_model,
    retriever=retriever,
    memory=memory
)

print("\n RAG Chatbot with Memory is Ready! Type 'exit' to stop.\n" + "="*50)

while True:
    query = input("\nUser Query: ")
    if query.lower() == 'exit':
        print("Exiting chat. Good bye!")
        break
    
    result = qa_chain({"question": query})
    
    print(f"\nAI Answer: {result['answer']}")
    
    print("\n Sources:")
    for doc in result["source_documents"]:
        print(f" - Page Content Preview: {doc.page_content[:150]}...")
    
    print("-" * 50)
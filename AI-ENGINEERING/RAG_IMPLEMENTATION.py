import os
from langchain_core.documents import Document
from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings 
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Document Converter
file = r"L:\AI_Engineer\02_Learning\AI_ENGINEER\Machine_Learning_Complete_Notes.pdf" 

print(f"[-] Parsing document with Docling: {file}")

converter = DocumentConverter()
result=converter.convert(file)
markdown_text=result.document.export_to_markdown()

doc = Document(page_content=markdown_text, metadata={"source": file})
print("[-] Splitting document into smart chunks...")


# Text Splitter
text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)
split_docs=text_splitter.split_documents([doc])

# print(f"[+] Generated {len(chunks)} chunks successfully!\n")

# Embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")
print("[-] Initializing Ollama Embeddings & FAISS Vector Store...")
# Vector Store
vectorstore=FAISS.from_documents(split_docs, embeddings)
print("[+] Vector store created and indexed!\n")

# Retrieval
retriever=vectorstore.as_retriever(search_type='similarity',search_kwargs={"k":3})

# llm and pipeline link setup

llm=ChatGroq(model="openai/gpt-oss-120b",temperature=0.2)

prompt=ChatPromptTemplate.from_messages([
    ("system","You are a helpful assistant that answers questions based on the provided context."),
    ("user","Context: {context}\n\nQuestion: {question}")
])

output=StrOutputParser()

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

rag_chain = (
        {
            "context": retriever | format_docs, 
            "question": RunnablePassthrough()
        }
        | prompt 
        | llm 
        | output
    )

while True:
    question=input("You:  ").strip()

    if question.lower() in ["exist","exit()","quit","end"]:
        print("Exiting the RAG loop.")
        break
    response = rag_chain.invoke(question)
    print(f"Assistant: {response}")


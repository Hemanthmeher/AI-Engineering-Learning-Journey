import os
from langchain_core.documents import Document
from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings 
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

# Document Converter
file = r"L:\AI_Engineer\02_Learning\AI_ENGINEER\Machine_Learning_Complete_Notes.pdf" 

if not os.path.exists(file):
    print(f"[!] Error: File not found at {file}")
else:
    print(f"[-] Parsing document with Docling: {file}")
    converter = DocumentConverter()
    result = converter.convert(file)
    markdown_text = result.document.export_to_markdown()

    doc = Document(page_content=markdown_text, metadata={"source": file})
    print("[-] Splitting document into smart chunks...")

    # Text Splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=150)
    split_docs = text_splitter.split_documents([doc])
    print(f"[+] Generated chunks successfully!\n")

    # Embeddings
    print("[-] Initializing Ollama Embeddings & FAISS Vector Store...")
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )

    # Vector Store
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    print("[+] Vector store created and indexed!\n")

    # Retrieval
    retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={"k": 3})

    # LLM and Pipeline Setup
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that answers questions based on the provided context."),
        ("user", "Context: {context}\n\nQuestion: {question}")
    ])

    output = StrOutputParser()

    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])

    # FEATURE CHAIN: Returns both Answer & Retrieved Source Chunks
    rag_chain = (
        RunnableParallel(
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
                "source_docs": retriever  # Tracks which PDF sections were used
            }
        )
        | RunnableParallel(
            {
                "answer": (lambda x: prompt.invoke({"context": x["context"], "question": x["question"]})) | llm | output,
                "source_docs": lambda x: x["source_docs"]
            }
        )
    )

    print("=" * 60)
    print("🤖 RAG Chatbot is Active & Ready with Source Citations!")
    print("Type your questions below. Type 'exit' or 'end' to quit.")
    print("=" * 60 + "\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in ["exit", "exit()", "quit", "end"]:
            print("Exiting the RAG loop.")
            break
        
        if not question:
            continue

        try:
            print("Assistant: Thinking...")
            result = rag_chain.invoke(question)
            print(f"\nAssistant: {result['answer']}\n")
            print("📁 [Source Citations / References Used]:")
            for i, doc in enumerate(result['source_docs'], 1):
                print(f"  {i}. Source File: {doc.metadata.get('source', 'Unknown')}")
            print("-" * 60)

        except Exception as e:
            print(f"[!] Error: {e}\n")
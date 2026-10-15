
# Section 8: Build AI Memory Systems (Vector Databases)
 
**Topics Covered:** 
1. Why LLMs Need Memory & Vector Databases
2. Embeddings, Vectors & Similarity Search
3. The 3 Core Phases of RAG (Ingestion, Retrieval, Generation)
4. Vector Indexing Algorithms (IVF & HNSW)
5. Local Vector Search with FAISS & LangChain
6. Cloud-Based Vector Databases with Pinecone

---

## 🚀 1. Core Concept: Why AI Needs Memory
Standard Large Language Models (LLMs) have static training data. They cannot natively know private documents, company files, or real-time data unless it is passed inside their context window. 
* **Vector Databases** act as an external memory layer for AI, storing document chunks as mathematical embeddings for lightning-fast similarity search.

---

## 🔍 2. Embeddings & Traditional vs. Vector DBs
* **Embeddings:** Raw text cannot be computed mathematically, so embedding models convert words and sentences into high-dimensional numerical arrays (vectors) that capture semantic meaning.
* **Traditional DBs (SQL/NoSQL):** Best for exact keyword matches and structured rows/columns.
* **Vector Databases:** Designed for similarity (semantic) searches where concepts match even if exact words differ.

---

## ⚙️ 3. The 3 Core Phases of RAG
1. **Ingestion:** Loading raw documents, splitting/chunking them into smaller pieces, converting them into vector embeddings, and storing them in a vector database.
2. **Retrieval:** When a user asks a question, the query is embedded and matched against the vector database using similarity metrics (Cosine Similarity, Euclidean Distance) to retrieve the most relevant text chunks.
3. **Generation:** The retrieved context chunks and the user's original query are combined into a prompt and fed to the LLM to generate a grounded, accurate answer.

---

## 🧠 4. Vector Indexing Algorithms (IVF & HNSW)
* **Why We Need Indices:** Brute-force nearest neighbor search is too slow for millions of vectors. Indexes organize data for fast lookups.
* **IVF (Inverted File Index):** Groups vectors into clusters. During search, it only looks inside the closest cluster, saving memory and time, but can occasionally miss edge-case matches.
* **HNSW (Hierarchical Navigable Small World):** Builds a multi-layer graph network. Provides extremely fast and high accuracy, but consumes more RAM.

---

## 💻 5. Practical Implementations

### **A. Local Vector Search using FAISS**
```python
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

docs = [
    Document(page_content="Stock market dropped 400 points on the recession worries today."),
    Document(page_content="Artificial intelligence is transforming software engineering rapidly."),
]

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_docs = text_splitter.split_documents(docs)

embeddings = OllamaEmbeddings(model="llama3.2")
vector_store = FAISS.from_documents(all_docs, embedding=embeddings)

query = "How much did the stock market fall?"
results = vector_store.similarity_search(query, k=1)

for res in results:
    print(res.page_content)


    
B. Cloud Vector DB using Pinecone
Python
import os
from pinecone import Pinecone, ServerlessSpec
from langchain_community.embeddings import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document

os.environ["PINECONE_API_KEY"] = "your-pinecone-api-key-here"

pc = Pinecone()
index_name = "vector-store-youtube"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

embeddings = OllamaEmbeddings(model="llama3.2")

docs = [
    Document(page_content="Stock market dropped 400 points on the recession worries today.", metadata={"category": "finance"}),
    Document(page_content="Odoo hackathon in Gujarat focused on backend development using FastAPI.", metadata={"category": "tech"}),
]

vector_store = PineconeVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    index_name=index_name
)

query = "Tell me about market crash"
results = vector_store.similarity_search(query, k=1, filter={"category": "finance"})

for res in results:
    print(res.page_content)
    print(res.metadata)
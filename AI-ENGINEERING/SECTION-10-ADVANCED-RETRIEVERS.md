Welcome to my learning notes for **Section 10**. In this section, I explored how standard vector search (similarity search) can sometimes hit limitations in real-world Retrieval-Augmented Generation (RAG) applications, and how **Advanced Retrievers** help solve these challenges to make AI systems much smarter and more accurate.

---

## 1. Limitations of Standard Vector Search
* **Redundancy:** Traditional vector retrieval often fetches top-k chunks that talk about the exact same thing, leading to duplicated and repetitive context for the LLM.
* **Vocabulary Mismatch:** Pure semantic search can miss exact keyword matches (like error codes, proper nouns, or unique product IDs) if the embedding vectors don't capture that exact token nuance.
* **Noise & Irrelevant Content:** Sometimes a retrieved document chunk contains a large paragraph where only a single line is actually relevant, wasting the LLM's context window.

---
### 🔍 A. Maximal Marginal Relevance (MMR)
* **Concept:** Regular similarity search often returns top-k chunks that talk about the exact same thing (redundancy). MMR solves this by balancing **relevance** to the user query with **diversity** among the retrieved documents.
* **Code Example:**
```python
from langchain.vectorstores import Chroma

# Using MMR as the search type instead of standard similarity
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 10, "lambda_mult": 0.5}
)

docs = retriever.invoke("What is Chroma vector database?")
Parameters Explained:

k = 3: Final ga manaki 3 documents kavali ani.

fetch_k = 10: Mundu vector store nundi top 10 relevant docs fetch chesi, vatilo nunchi best diverse 3 select chesthundi.

lambda_mult: Diversity ki mariyu relevance ki madhya balance (0.5 ante equal priority).

🔀 B. Multi-Query Retriever
Concept: If a user's query is poorly phrased or ambiguous, standard search might miss matching documents. The Multi-Query retriever uses an LLM to automatically generate multiple sub-queries from different perspectives, fetches results for all of them, and combines/deduplicates the output.

Code Example:

Python
from langchain.retrievers import MultiQueryRetriever
from langchain_groq import ChatGroq

# Initialize LLM for query generation
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# Create Multi-Query Retriever from base vectorstore retriever
retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    llm=llm
)

docs = retriever.invoke("How do I store embeddings?")
✂️ C. Contextual Compression Retriever
Concept: Standard retrievers return full document chunks or large paragraphs, but much of that text might be noise. Contextual compression passes retrieved documents through a compressor/extractor to strip away irrelevant text, leaving only the exact relevant sentences for the LLM.

Code Example:

Python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# Setup an extractor compressor using LLM
compressor = LLMChainExtractor.from_llm(llm)

# Wrap it around the base retriever
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever()
)

compressed_docs = compression_retriever.invoke("Tell me about vector stores.")
📊 D. BM25 Retriever (Keyword-Based & TF-IDF Foundation)
Concept: While semantic search understands meaning, BM25 excels at exact keyword matching (e.g., error codes, IDs, exact names) using TF-IDF principles (Term Frequency & Inverse Document Frequency) with length normalization.

Code Example:

Python
from langchain_community.retrievers import BM25Retriever

# Create BM25 retriever directly from raw document list
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 2  # Set top-k results

docs = bm25_retriever.invoke("Chroma collection setup")


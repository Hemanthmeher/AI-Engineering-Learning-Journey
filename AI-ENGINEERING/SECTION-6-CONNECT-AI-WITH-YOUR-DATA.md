# Section 6: Connect AI with Your Data (Load, Process & Prepare) 🚀

This repository documents my learning progress and hands-on code implementations for **Section 6** of the AI Engineering Bootcamp. In this section, I explored how modern AI applications ingest external data, handle document loaders, and utilize advanced text-splitting strategies for Retrieval-Augmented Generation (RAG).

---

## 📚 Topics Covered

1. **Document Loaders Explained**
   - Understanding how AI reads unstructured and structured data.
   - Using built-in LangChain document loaders for PDFs, websites, ArXiv, and Wikipedia APIs.

2. **Text Splitters & Chunking Strategies**
   - Why text splitting is essential for staying within LLM context windows and improving retrieval accuracy.
   - Managing `chunk_size` and `chunk_overlap` effectively.

3. **Advanced Splitting Techniques**
   - **Character Text Splitter:** Basic split based on character count and single separators.
   - **Recursive Character Text Splitter:** Smart hierarchical splitting using a priority list of separators (`\n\n`, `\n`, `" "`, `""`).
   - **Markdown Text Splitter:** Structuring and splitting markdown documents based on header hierarchies (`#`, `##`, `###`).
   - **Token Text Splitter:** Precise splitting based on LLM token limits rather than raw character counts.
   - **Semantic Text Splitter (`SemanticChunker`):** Context-aware splitting that detects semantic shifts and topic changes using embedding similarities.

---

## 💻 Code Implementations & Examples

### 1. Character Text Splitter
```python
from langchain_text_splitters import CharacterTextSplitter

char_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=100,
    chunk_overlap=20
)

text = "Idi oka pedda paragraph...\n\nIdi inkoka paragraph..."
chunks = char_splitter.create_documents([text])
print(f"Total Chunks: {len(chunks)}")


2. Recursive Character Text Splitter (Most Recommended)
Python
from langchain_text_splitters import RecursiveCharacterTextSplitter

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    separators=["\n\n", "\n", " ", ""]
)

text = "Heading text here.\n\nParagraph one content goes here..."
chunks = recursive_splitter.create_documents([text])


3. Markdown Text Splitter
Python
from langchain_text_splitters import MarkdownHeaderTextSplitter

markdown_text = """
# Introduction
Main heading text here.

## Section 1
Sub-heading details here.
"""

headers_to_split_on = [("#", "Header 1"), ("##", "Header 2")]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_chunks = markdown_splitter.split_text(markdown_text)



4. Token Text Splitter
Python
from langchain_text_splitters import TokenTextSplitter

token_splitter = TokenTextSplitter(chunk_size=50, chunk_overlap=10)
sample_text = "Artificial Intelligence and LangChain framework make RAG pipelines easy."
token_chunks = token_splitter.create_documents([sample_text])



5. Semantic Text Splitter (SemanticChunker)
Python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(openai_api_key="YOUR_OPENAI_API_KEY")

semantic_splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="percentile"  # Options: "standard_deviation", "interquartile", "gradient"
)

text = """
Artificial Intelligence is transforming the world rapidly. Machine learning algorithms allow computers to learn from data.
Python is the most popular programming language for AI development.
On the other hand, cooking is an art of making delicious food.
"""

docs = semantic_splitter.create_documents([text])

# Iterating and printing chunks cleanly
for i, doc in enumerate(docs):
    print(f"--- Chunk {i+1} ---")
    print(doc.page_content.strip())
    print()


🛠️ Key Takeaways & Differences
Character vs. Token Splitters: Character splitters count raw characters (letters/spaces), whereas Token splitters account for model tokenization limits to prevent API truncation errors.

Recursive Splitter Logic: Falls back step-by-step from paragraphs (\n\n) to lines (\n), words ( ), and characters ("") to keep semantic context intact.

Semantic Chunker: Instead of slicing by fixed sizes, it analyzes vector distances between sentences to split text precisely where the topic changes.
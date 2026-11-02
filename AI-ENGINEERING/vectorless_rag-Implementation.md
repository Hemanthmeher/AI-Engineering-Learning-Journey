# 🚀 Building a Vectorless RAG System 

In this section, I started building a **Vectorless RAG (Retrieval-Augmented Generation)** system from scratch. Instead of using traditional vector databases (like ChromaDB, FAISS) and complex embedding math, this approach treats documents like a human reader—extracting text, breaking it into logical sections using LLM reasoning, saving it as a clean JSON index, and performing smart reasoning-based retrieval!


---

## 🏗️ Lecture 102: Understanding the Project Architecture (6-Step System Flow)
Before writing code, we mapped out the complete system architecture to understand how data flows from a raw PDF file to an intelligent AI response:

1. **Step 1 & 2: PDF Ingestion & Page Extraction** — Reading the raw PDF file page-by-page using Python and preserving page numbers for future source citations.
2. **Step 3 & 4: LLM-Powered Section Extraction** — Passing the raw text to an LLM so it can logically split the document into clean sections with titles, main content, and page numbers.
3. **Step 5: Vectorless Indexing & JSON Caching** — Storing the parsed section metadata into a structured JSON file (`vectorless_index.json`) so we don't have to re-process the PDF on every run (saves time and API costs!).
4. **Step 6: Reasoning-Based Retrieval** — When a user asks a question, the LLM reads the JSON index summaries and applies reasoning to select the exact relevant section instead of relying on vector similarity math.
5. **Step 7 & 8: Grounded Answer Generation** — Pulling the actual content of the selected section and generating a precise, fact-based answer with page citations.

---

## 💻 Lecture 103: Loading & Processing Documents (Implementation)

Here is the Python code I wrote to handle PDF loading, intelligent section parsing using LLM structured prompts, and JSON caching mechanisms:

```python
import json
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from pypdf import PdfReader
from dotenv import load_dotenv

# Load environment variables (API keys)
load_dotenv()

# Initialize the LLM (Using Groq model)
llm = ChatGroq(model="openai/gpt-oss-120b")


# --- Step 1: Load PDF & Extract Page-by-Page Text ---
def load_pdf(filepath):
  """Opens a PDF file, reads it page by page, and stores each page number

  along with its raw text content into a clean list of dictionaries.
  """
  try:
    reader = PdfReader(filepath)
    pages = []
    for pagenum, page in enumerate(reader.pages):
      text = page.extract_text()
      pages.append({"page_number": pagenum + 1, "text": text})
    return pages
  except Exception as e:
    print(f"Error loading PDF: {e}")
    return None


# --- Step 2: Intelligent Section Extraction ---
def extract_section(pages, llm):
  """Takes all extracted pages, combines them into a single string with page markers,

  and asks the LLM to parse it into logical sections (Title, Content, Page Number).
  """
  # Combine page texts together with clear page markers
  full_document = "\n".join(
      [f"--- Page {p['page_number']} ---\n{p['text']}" for p in pages]
  )

  # Define the prompt instructing the LLM to act as a document parser
  prompt = ChatPromptTemplate.from_messages([
      (
          "system",
          "You are an expert AI text extractor and document parser. "
          "Read the provided document text carefully and extract logical sections. "
          "For each section, provide the exact 'title', the full 'content' text belonging to that section, "
          "and the corresponding 'page' number where it appears.",
      ),
      (
          "user",
          "Here is the document content with page markers:\n\n{document}\n\n"
          "Extract the sections with their title, content, and page number.",
      ),
  ])

  chain = prompt | llm
  response = chain.invoke({"document": full_document})
  return response.content


# --- Step 3: Save Extracted Sections to JSON (Caching) ---
def save_json(data, filepath):
  """Saves the extracted document index into a structured JSON file

  so we don't have to re-process the PDF every time.
  """
  try:
    with open(filepath, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=4)
    print(f"Data saved to {filepath}")
  except Exception as e:
    print(f"Error saving JSON: {e}")


# --- Step 4: Load JSON Cache ---
def load_json(filepath):
  """Loads the pre-processed JSON index back into Python

  for fast retrieval and reasoning.
  """
  try:
    with open(filepath, "r", encoding="utf-8") as f:
      data = json.load(f)
    return data
  except Exception as e:
    print(f"Error loading JSON: {e}")
    return None
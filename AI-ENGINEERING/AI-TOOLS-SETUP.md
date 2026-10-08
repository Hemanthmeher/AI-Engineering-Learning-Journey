# 🚀 Section 4: AI Tools Setup — API Keys & Environment Configuration

---

## 📌 Section Overview

In modern AI Engineering, applications rely on an ecosystem of specialized external services: high-speed LLM inference, vector search indices, web tools, and tracing platforms.

This section covers the setup, configuration, API key generation, and secure environment integration for the fundamental infrastructure used across production Agentic AI and RAG pipelines.

---

## 🧠 Services & Tools Configured

| Service / Tool | Category | Core Purpose & Use Case |
| :--- | :--- | :--- |
| **HuggingFace** | Pretrained Models | Access to open-weight LLMs, specialized embeddings, and open-source models via Inference APIs. |
| **LangSmith** | AI Observability | Tracing, debugging, evaluating, and monitoring LLM chains and LangGraph agents in real-time. |
| **Groq** | Ultra-Fast LLM Inference | LPU-powered inference delivering ultra-low latency for open models like Llama 3 and Mixtral. |
| **Weaviate** | Vector Database | Hybrid search and vector storage engine optimized for complex RAG document retrieval. |
| **Tavily AI** | Web Search API | Purpose-built search engine for AI Agents to fetch real-time, clean web content without HTML scraping bloat. |
| **Pinecone** | Serverless Vector DB | Cloud-native, high-scalability vector database for production similarity search and embedding storage. |

---

## 🛠️ Detailed Concepts & Practical Implementations

### 1. API Keys Security (`.env` vs Code)
- **Hardcoding Danger:** API keys committed to public repositories (like GitHub) lead to key revocation, unauthorized usage, and security compliance failures.
- **Environment Isolation:** Keys are stored in an uncommitted `.env` file and injected into runtime environment variables dynamically using `python-dotenv`.

---

### 2. Complete Environment Configuration (`.env`)

Create a local `.env` file at the root of the project with the following configuration:

```env
# --- LLM API Keys ---
OPENAI_API_KEY=sk-proj-your-openai-api-key
GROQ_API_KEY=gsk_your_groq_api_key
HUGGINGFACEHUB_API_TOKEN=hf_your_huggingface_token

# --- Vector Database Configurations ---
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=us-east-1

WEAVIATE_URL=[https://your-weaviate-instance.weaviate.network](https://your-weaviate-instance.weaviate.network)
WEAVIATE_API_KEY=your_weaviate_api_key

# --- Web Search Tools ---
TAVILY_API_KEY=tvly-your_tavily_search_api_key

# --- AI Observability & Tracing (LangSmith) ---
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=[https://api.smith.langchain.com](https://api.smith.langchain.com)
LANGCHAIN_API_KEY=lsv2_pt_your_langsmith_api_key
LANGCHAIN_PROJECT=ai-engineering-learning-journey
3. Production Verification Script (test_tools_setup.py)
Python integration script to verify environment variable loading and validate API connectivity across Groq, Tavily, and LangSmith:

Python
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import TavilySearchResults

# 1. Load Environment Variables from .env
load_dotenv()

def verify_environment():
    required_keys = [
        "GROQ_API_KEY",
        "TAVILY_API_KEY",
        "LANGCHAIN_API_KEY"
    ]
    
    print("🔍 Checking Environment Variables...")
    for key in required_keys:
        val = os.getenv(key)
        if not val:
            raise ValueError(f"❌ Missing required environment variable: {key}")
        print(f"  ✓ {key} is set.")

def test_groq_and_tavily():
    print("\n⚡ Testing Groq Ultra-Fast Inference...")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    response = llm.invoke("State the core purpose of a Vector Database in 10 words.")
    print("Groq Response:", response.content)

    print("\n🌐 Testing Tavily Real-Time Web Search Tool...")
    search_tool = TavilySearchResults(max_results=1)
    search_result = search_tool.invoke({"query": "Latest LangGraph updates"})
    print("Tavily Search Output:", search_result)

if __name__ == "__main__":
    verify_environment()
    test_groq_and_tavily()
    print("\n✅ All AI Tools & API Configurations Verified Successfully!")
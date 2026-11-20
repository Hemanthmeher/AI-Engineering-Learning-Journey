# Building My First AI Research Agent (Part 1: Query Generation to Summarization)

Today I started building an end-to-end **AI Research Agent** using LangGraph, Groq, and Tavily. Instead of just building a simple chatbot, the goal here is to create a workflow that takes a topic, generates smart search queries on its own, fetches real-time data from the internet, and turns that raw web content into structured insights.

So far, I have completed the core building blocks (environment setup + the 3 main LangGraph nodes) up to the summarization step.

---

## 1. Project Setup & Dependencies
First, I set up a clean virtual environment and organized the project into modular files (`Tools.py` and `nodes.py`) so the code stays easy to maintain and debug. Along with `langgraph`, `langchain-groq`, and `python-dotenv`, I installed `tavily-python` to give the agent live internet search capabilities.

---

## 2. Generating Smart Search Queries (`generate_queries` Node)
When researching any topic, a single raw user prompt isn't enough—we need focused search queries.

- Initially, asking the LLM to generate 3 queries gives plain text with bullet points or numbering (`1.`, `2.`, `-`), which requires messy string cleaning (`.split()`, `.replace()`, `.strip()`).
- To make this cleaner and reliable, I used **Pydantic (`BaseModel`)** with **`llm.with_structured_output(SearchQueries)`**.
- Now, instead of parsing raw text, the LLM directly returns a validated Python list of 3 search queries (`response.queries`). No extra string cleanup needed.

---

## 3. Connecting to Real-Time Internet Data (`Tools.py` & `search_node`)
LLMs only know what they were trained on, so I integrated the **Tavily Search API** to pull fresh web results.

- **`Tools.py` (`search_tool`):** Built a helper function using `TavilyClient` that searches a query (`max_results=5`) and extracts only the fields we actually care about (`title`, `content`, and `url`) using safe dictionary `.get()` lookups.
- **`search_node`:** Loops through the generated queries, skips any empty strings, collects results across all queries using `.extend()` (so everything stays in a single flat list rather than nested lists), and slices the output (`all_results[:5]`) to keep the top 5 results.

---

## 4. Turning Raw Web Data into Insights (`summarize_node`)
Raw search results can be huge and easily overflow the LLM's context limit or waste tokens.

- **Token/Character Guardrail:** Before sending the search results to the LLM, I capped each article snippet at 500 characters (`r.get("content", "")[:500]`) and set an overall limit of `MAX_CHARS = 4000`.
- **Structured Synthesis:** Passed the cleaned research text into the Groq LLM (`ChatGroq`) with a clear prompt to extract:
  - 5 key insights
  - 3 important facts
  - A short conclusion

---

## Key Takeaways So Far
- **`with_structured_output()` saves a lot of headache:** Defining a Pydantic schema upfront beats writing fragile string-parsing logic every single time.
- **`.extend()` vs `.append()` matters in search loops:** When merging multiple lists of search results, `.extend()` keeps the list flat so slicing (`[:5]`) works properly.
- **Always cap external web content:** Trimming raw search text before feeding it into a summarization prompt prevents context overflow and keeps responses fast.

---

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from Nodes import generate_queries, search_node, summarize_node

class ResearchState(TypedDict):
    topic: str
    queries: list[str]
    results: list[dict]
    summary: str


builder = StateGraph(ResearchState)
builder.add_node("generate_queries", generate_queries)
builder.add_node("search", search_node)
builder.add_node("summarize", summarize_node)

builder.add_edge(START, "generate_queries")
builder.add_edge("generate_queries", "search")
builder.add_edge("search", "summarize")
builder.add_edge("summarize", END)

graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({"topic": "Tell me About Movie Ramanayam released in 2026"})
    print(result["summary"])


import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from Tools import search_tool

load_dotenv()

class SearchQueries(BaseModel):
    queries: list[str] = Field(description="3 concise web search queries for the topic")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

structured_llm = llm.with_structured_output(SearchQueries)

def generate_queries(state):
    topic = state["topic"]
    prompt = f"""Generate 3 smart search queries for researching this topic: {topic}

Return ONLY valid JSON in this exact format:
{{"queries": ["query 1", "query 2", "query 3"]}}"""

    raw = llm.invoke(prompt)
    content = raw.content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    data = json.loads(content)
    queries = [str(q) for q in data.get("queries", [])]
    return {"queries": queries}

def search_node(state):
    queries = state["queries"]
    all_results = []

    for q in queries:
        if not q.strip():
            continue

        results = search_tool(q)
        all_results.extend(results)

    return {"results": all_results[:5]}

def summarize_node(state):
    topic = state["topic"]
    results = state["results"]

    MAX_CHARS = 4000 

    content = ""
    for r in results:
        if len(content) < MAX_CHARS:
            content += r.get("content", "")[:500] + "\n\n"

    prompt = f"""
Summarize the following research for: {topic}

Research Content:
{content}

Give:
- 5 key insights
- 3 important facts
- short conclusion
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"summary": response.content}
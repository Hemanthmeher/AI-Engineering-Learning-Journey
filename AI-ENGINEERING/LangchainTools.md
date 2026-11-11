# AI Engineering Learning Notes: LangChain Tools & Agents

## 1. Introduction to Tools in LangChain

In Agentic AI systems, Large Language Models (LLMs) are brilliant at reasoning and understanding intent, but they lack real-time data access and the ability to execute specific actions. **Tools** bridge this gap by giving LLMs *hands and eyes* to interact with the external world (web, databases, internal APIs).

---

## 2. Built-in Tools

Built-in tools are pre-configured, ready-to-use components provided directly out-of-the-box by LangChain and its community libraries. We don't need to write the underlying logic from scratch; we simply import, configure, and bind them.

### A. Wikipedia Tool (`WikipediaQueryRun`)

Used to fetch factual information and summaries from Wikipedia articles. It relies on a two-part architecture:
1. **`WikipediaAPIWrapper` (The Backend Engine):** Handles direct **API** calls, parameter configurations (e.g., `top_k_results=5`, `doc_content_chars_max=**500**`), and raw data extraction.
2. **`WikipediaQueryRun` (The Tool Wrapper):** Wraps the **API** engine into a standard LangChain tool format so that LLMs can recognize, invoke, and read its metadata (`name`, `description`).

**Code Implementation:** ```python from langchain_community.tools import WikipediaQueryRun from langchain_community.utilities import WikipediaAPIWrapper

# 1. Configure the API wrapper engine

api_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=**500**)

# 2. Wrap it into a LangChain tool

wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

# Test execution

print(wiki_tool.run(*Artificial Intelligence*))
- Tavily Search Tool (TavilySearchResults)
Unlike general search engines or DuckDuckGo (which can sometimes return messy **HTML** or hit anti-scraping blocks), Tavily is an AI-optimized search engine built specifically for LLMs and AI Agents. It returns clean, structured **JSON** payloads containing URLs, titles, and content snippets.

Code Implementation:

Python import os from langchain_community.tools.tavily_search import TavilySearchResults

# Set API key

os.environ[*TAVILY_API_KEY*] = *your-tavily-api-key*

# Initialize Tavily search tool

tavily_tool = TavilySearchResults(max_results=3)

# Test execution

response = tavily_tool.run(*latest trends in Agentic AI **2026***) print(response) ## Custom Tools (From Scratch) When built-in tools aren't enough (e.g., querying internal company databases, executing custom business logic, or running proprietary calculations), we write Custom Tools.

In LangChain, any Python function can be converted into an AI tool using the @tool decorator.

Key Rule for Custom Tools: The Docstring is Mandatory: The **LLM** does not read the function body; it reads the function Docstring and Type Hints to understand what the tool does, when to use it, and what arguments to pass.

Code Implementation:

Python from langchain_core.tools import tool

@tool
def calculate_employee_bonus(salary: float, performance_score: int) -> str:
    """Calculates the end-of-year bonus for an employee based on their annual salary 
    and performance rating scale from 1 to 5.
    """
    if performance_score >= 4:
    bonus = salary * 0.15
    else:
    bonus = salary * 0.05
    return f*Calculated Bonus: ${bonus:.2f}*

# Inspecting tool metadata readable by the LLM

print(calculate_employee_bonus.name)        # 'calculate_employee_bonus' print(calculate_employee_bonus.description) # Docstring description ## How LLMs Interact with Tools (Under the Hood Execution Flow) LLMs are purely text-in, text-out models. They cannot execute Python code directly. Instead, tool execution follows a structured agentic cycle:

Schema Binding: We bind tools to the model using .bind_tools([tool_list]). LangChain converts function signatures, names, and docstrings into **JSON** schemas and passes them to the **LLM** in the system prompt payload.

Intent Detection & Argument Extraction: When a user passes a query (e.g., *What is the bonus for $80k salary with rating 5?*), the **LLM** analyzes the query and matches it with the correct tool description.

Structured Tool Call Return: Instead of returning plain text, the **LLM** outputs a structured **JSON** object (tool_calls) containing the target function name and extracted arguments (salary=**80000**.0, performance_score=5).

Execution & Final Response: The agent runner executes the Python function locally with those arguments, feeds the output back into the **LLM** context, and the model translates the raw output into a natural, conversational response for the user.
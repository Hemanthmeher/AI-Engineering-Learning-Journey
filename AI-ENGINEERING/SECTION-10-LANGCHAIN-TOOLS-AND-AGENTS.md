# SECTION-10: LangChain Tools & Agents - Complete Learning Guide

## 1. Introduction to LangChain Tools (Turn AI into Action)
Normally, Large Language Models (LLMs) are like "brains in a box"—they can process text and generate responses based on their training data, but they cannot interact with the real world (e.g., check live weather, calculate math, search the web, or access databases). 
* **Tools** bridge this gap. A Tool is essentially a Python function wrapped in a way that an LLM can understand, choose, and execute when it needs external capabilities.

---

## 2. Built-in Tools (Ready-Made Capabilities)
LangChain provides a rich set of pre-built community tools so you don't have to write everything from scratch. These connect LLMs to Wikipedia, Arxiv, DuckDuckGo, Tavily Web Search, and more.

### Example: Using Wikipedia Built-in Tool
```python
from langchain_groq import ChatGroq
from langchain_community.tools.wikipedia import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langgraph.prebuilt import create_react_agent

# 1. Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 2. Setup Built-in Tool
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

tools = [wikipedia_tool]

# 3. Create Agent
agent_executor = create_react_agent(llm, tools)

# 4. Invoke
response = agent_executor.invoke({"messages": [("user", "Tell me about Albert Einstein")]})
print(response["messages"][-1].content)

---

## 5. Building Custom ReAct Agents with Multiple Custom Tools
When you want to give an LLM multiple capabilities (like mathematical calculations and string manipulation), you can write multiple custom tools using the `@tool` decorator and pass them together into LangGraph's `create_react_agent`.

### Complete Code Example: Multi-Tool Agent
```python
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# 1. Custom Calculator Tool
@tool
def calculator(question: str) -> str:
    """
    A calculator tool that can perform mathematical calculations.
    Args:
        question (str): The mathematical question to be answered.
    Returns:
        str: The answer to the mathematical question.
    """
    try:
        result = eval(question)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

# 2. Custom String Reversal Tool
@tool
def reverseString(input_string: str) -> str:
    """
    A tool that reverses the input string.
    Args:
        input_string (str): The string to be reversed.
    Returns:
        str: The reversed string.
    """
    return input_string[::-1]

# 3. Initialize LLM and Agent with Multiple Tools
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)
agent = create_react_agent(model=llm, tools=[calculator, reverseString])

# 4. Interactive Chat Loop
print("Jarvis Agent Ready! Type 'exit' to quit.")
while True:
    question = input("You: ").strip()
    if question.lower() in ["exit", "quit"]:
        print("Exiting the chat. Goodbye!")
        break
    
    response = agent.invoke({"messages": [("user", question)]})
    print(f"Jarvis: {response['messages'][-1].content}\n")
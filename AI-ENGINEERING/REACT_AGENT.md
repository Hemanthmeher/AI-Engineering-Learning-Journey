Section 34: ReAct Agents with Multiple Tools — My Learning Journey Notes In this section, I learned how to build a ReAct (Reasoning + Acting) Agent that goes beyond a single tool and can orchestrate multiple tools (such as online search and math calculations) in a single loop to solve complex multi-step problems.

1. Core Concept & Why Multiple Tools?
  Real-World Complexities: Real-world user queries often require more than one action. For example, a user might ask for live factual data (which requires a web search) and then ask to perform calculations on those numbers (which requires math tools like add or multiply).

ReAct Workflow: Instead of guessing or hallucinating an answer, the agent analyzes the user question (Reasoning), decides which tool is best suited for the task, invokes it (Acting), and repeats the process until the final answer is achieved.

2. Tools Setup & Integration
  I used langchain and langgraph to define custom mathematical tools (add, multiply) and integrated DuckDuckGoSearchRun (online_search) for fetching real-time data.

Using llm.bind_tools(tools), I connected these tools to the LLM so the model knows what tools are available and automatically decides when to trigger them based on the system prompt.

3. Building the LangGraph Workflow for Multi-Tool Agent
  To orchestrate the multi-tool agent, I constructed a custom StateGraph:

State Management: Utilized MessagesState to track the conversation history and tool-call payloads.

Agent Node (function_1): Combines the system prompt and user messages, invokes the bound LLM, and decides whether to call a tool or reply directly.

Conditional Routing (tools_condition): Built-in LangGraph logic that automatically routes the execution flow to the tools node if the LLM requests a tool call.

ToolNode (tools): Executes the requested tool (whether it's search or math) and returns the output back to the agent node.

Looping Mechanism: After the tool executes, the output goes back to the Agent node so the model can process the result and formulate the final answer.
from langchain_core.messages import HumanMessage, SystemMessage from langchain_community.tools import DuckDuckGoSearchRun from langchain.tools import tool from langgraph.graph import MessagesState, StateGraph, END, START from langgraph.prebuilt import ToolNode, tools_condition from langchain_groq import ChatGroq

search = DuckDuckGoSearchRun()

@tool
def online_search(query: str) -> str:
    """
Search the web for real-time information, recent events, factual data, or specific historical facts using DuckDuckGo.

```
Args:
    query (str): The search query string to look up on the internet.
"""
result = search.invoke(query)
return result
```

@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two integers.

```
Args:
    a (int): The first integer.
    b (int): The second integer.
```

```
Returns:
    int: The product of a and b.
"""
return a * b
```

@tool
def add(a: int, b: int) -> int:
    """
    Add two integers.

```
Args:
    a (int): The first integer.
    b (int): The second integer.
"""
return a + b
```

tools = [online_search, add, multiply]

llm = ChatGroq(model='openai/gpt-oss-120b', temperature=1) llm_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = SystemMessage(
    content="You are a helpful assistant tasked with using search and performing arithmetic on a set of inputs."
)

def function_1(state: MessagesState):
    user_question = state["messages"]
input_question = [SYSTEM_PROMPT] + user_question response = llm_tools.invoke(input_question) return { "messages": [response] }

workflow = StateGraph(MessagesState)

workflow.add_node("Agent", function_1)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("Agent")
workflow.add_conditional_edges("Agent", tools_condition) workflow.add_edge("tools", "Agent")

Graph = workflow.compile()

user_q = input("Ask question: ")
inputs = {'messages': [HumanMessage(content=user_q)]} response = Graph.invoke(inputs)

print(response)
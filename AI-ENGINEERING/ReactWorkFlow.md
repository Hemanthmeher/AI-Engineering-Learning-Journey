# Section 31: Mastering ReAct Agents in LangGraph 🚀

In this section, I explored how to build a fully functional **ReAct (Reason + Act) Agent** using LangGraph, Custom Tools, and LangGraph Prebuilt nodes. Instead of just getting direct answers from an LLM, the agent can now dynamically decide when to use a tool, execute it, and return the final answer.

---

## 1. What is a ReAct Agent?
**ReAct** stands for **Reason + Act**. 
- **Reasoning:** The LLM looks at the user's question, thinks about whether it has the direct answer or if it needs external help.
- **Acting:** If it needs help, it generates a `tool_call` request (Action).
- **Observation & Loop:** The tool runs, returns the result, and the agent uses that observation to formulate the final answer.

---

## 2. Core Components We Built

### A. Custom Tools (`@tool`)
To give superpowers to our LLM, we define custom Python functions decorated with `@tool`. The docstring (`"""..."""`) is critical because the LLM reads it to understand what the tool does and when to invoke it.

```python
from langchain_core.tools import tool

@tool
def search_weather(query: str) -> str:
    """Search the web for real-time weather information."""
    if "tadapalligudem" in query.lower():
        return "The current temperature in Tadepalligudem is 32°C and sunny."
    return "The temperature is 25°C and cloudy."

- Binding Tools to **LLM** (bind_tools)We connect our tools to the Groq **LLM** so it knows which tools are available:Pythonfrom langchain_groq import ChatGroq

llm = ChatGroq(model=*openai/gpt-oss-120b*)
llm_with_tool = llm.bind_tools([search_weather])
- The Agent Node (call_model)This node invokes the **LLM** with the current conversation state (MessagesState) and returns the model's response back to the graph state.Pythonfrom langgraph.graph import MessagesState

def call_model(state: MessagesState):
    messages = state[*messages*]
    response = llm_with_tool.invoke(messages)
    return {*messages*: [response]}
- ToolNode & tools_condition (The Magic of LangGraph)ToolNode: This is a pre-built node in LangGraph that automatically intercepts the **LLM**'s tool_calls request, executes the corresponding Python tool function, and returns a ToolMessage.tools_condition: A smart pre-built router function. It inspects the **LLM**'s latest message:If there is a tool_call $\rightarrow$ routes to the *tools* node.If no tool is needed (direct answer) $\rightarrow$ routes to **END**.3. Complete ReAct Agent Workflow CodeHere is the complete production-ready script combining all components into a StateGraph workflow:Pythonfrom langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, MessagesState, **START**, **END**
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq

# 1. Define Tools

@tool
def search_weather(query: str) -> str:
    ""*Search the web for real-time information.*"*
    if *tadapalligudem* in query.lower() or *weather* in query.lower():
    return *The current temperature in Tadepalligudem is 32°C and sunny.*
    return *The temperature is 25°C and cloudy."

tools = [search_weather]

# 2. Initialize LLM and Bind Tools

llm = ChatGroq(model=*openai/gpt-oss-120b*) llm_with_tool = llm.bind_tools(tools)

# 3. Define Agent Node Function

def call_model(state: MessagesState):
    messages = state[*messages*]
    response = llm_with_tool.invoke(messages)
    return {*messages*: [response]}

# 4. Build LangGraph Workflow

workflow = StateGraph(MessagesState)

# Add Nodes

workflow.add_node(*agent*, call_model) workflow.add_node(*tools*, ToolNode(tools))

# Add Edges & Conditional Routing

workflow.add_edge(**START**, *agent*) workflow.add_conditional_edges(*agent*, tools_condition) workflow.add_edge(*tools*, *agent*)  # Loop back to agent after tool execution

# Compile the App

app = workflow.compile()

# 5. Run the Workflow

inputs = {*messages*: [HumanMessage(content=*what is the weather in tadepalligudem*)]} output = app.invoke(inputs)

print(*Final Output from **LLM**:*, output[*messages*][-1]
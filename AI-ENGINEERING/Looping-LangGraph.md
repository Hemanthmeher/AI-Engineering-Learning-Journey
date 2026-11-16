### **My LangGraph Journey — Daily Notes (Lecture 140)**

**Topic:** Looping in LangGraph — How AI Improves Its Own Answers

**Date:** November 16, 2026

#### **1\. Asalu Ee Topic Enduku Important? (Core Concept)**

Idi varaku manam chusinappudu, oka LLM agent ki prompt ivvagane adi okate attempt lo answer ichi aagipoyedi. Kani real-world lo avi chala sarlu mistakes chestayi, ledha full information ivvalevu.

Ikkade **Looping** vastundi. Looping ante em ledu—AI tana work ni tane cross-check chesukuntu, thappulu unte rectifying chestu, final ga 100% correct output vache varaku oka loop laaga run avvadam. Ee concept valla AI ki "Self-improving" behavior vastundi.

#### **2\. Workflow Architecture & Flow**

Pratham sir lecture lo chupinchina diagram prakaram flow ela untundo idi:

1.  **Start:** User input `__start__` state lo enter avtundi.

2.  **Agent Node (`llmwithtool` / `agent`):** Model question ni chusi, direct answer ivvocha leda tools use cheyyala ani decide chestundi.

3.  **Tools Node (`tools` / `mytools`):** Avasaram anipisthe external search tools ki velli information fetch chestundi.

4.  **The Magic Loop:** Normal ga aithe ikkaditho aagipovali, kani ikkada manam tool output ni **malli venakki agent (LLM) ke pass chestunnam** (`workflow.add_edge("tools", "agent")`).

5.  **Re-evaluation:** Agent aa kotha tool output ni chusi, inka emaina info kavala or final answer ready ayinda ani malli check chesukuntundi. Correct anipiste appude loop aagi `__end__` ki veltundi.

#### **3\. Complete Python Code**

Nenu practice chesina and notes lo rasukunna code idi. Clear ga chusi understand chesukovadaniki chala easy ga untundi:

Python

```
from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

# Step 1: Initialize model and bind tools
model = ChatOpenAI(model="gpt-4o", temperature=0)

def search_tool(query: str) -> str:
  """Use this tool to search for real-time information."""
  return f"Result for {query}: LangGraph supports cyclical graphs for looping agentic workflows."

tools = [search_tool]
model_with_tools = model.bind_tools(tools)

# Step 2: Define the Agent / LLM node
def call_model(state: MessagesState):
  messages = state["messages"]
  response = model_with_tools.invoke(messages)
  return {"messages": [response]}

# Step 3: Build the StateGraph workflow
workflow = StateGraph(MessagesState)

# Add nodes to graph
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

# Set entry point
workflow.set_entry_point("agent")

# Add conditional edges (deciding between tool call or ending)
workflow.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})

# THIS IS THE LOOP: Connecting tools output back to the agent node!
workflow.add_edge("tools", "agent")

# Compile the graph workflow app
app = workflow.compile()

# Step 4: Stream and run the workflow
inputs = {
    "messages": [HumanMessage(content="Explain how looping works in LangGraph.")]
}

for event in app.stream(inputs, stream_mode="values"):
  event["messages"][-1].pretty_print()
```
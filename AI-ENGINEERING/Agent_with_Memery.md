# Memory Systems in LangGraph (Section 33)

## 1. Why Do We Need Memory in LangGraph?
By default, LangGraph workflows are **stateless**. When we invoke a graph with a message, it processes the input, gives an output, and immediately forgets everything. If we ask a follow-up question, it treats it as a completely new conversation.

To make an AI agent remember past interactions, tool outputs, and context across multiple turns, we need to add **Persistence (Memory)** to the graph.

---

## 2. Core Concepts Learned

* **Checkpointer (`MemorySaver`):** 
  In LangGraph, memory is managed using a checkpointer. `MemorySaver` is a built-in checkpointer that saves the entire state of the graph (all messages, tool calls, and responses) after every step.
* **In-Memory Storage (RAM):** 
  `MemorySaver` stores conversation history temporarily in the system's RAM. It is great for local development and testing, but if the script stops or the server restarts, the memory is wiped out. *(For permanent storage in production, we replace `MemorySaver` with `SqliteSaver` or `PostgresSaver`).*
* **Thread ID (`thread_id`):** 
  To keep different user conversations separate, LangGraph uses a `thread_id` inside a `config` dictionary. Each `thread_id` acts as an isolated chat session.
* **Agent Memory with Tools (Mini Project 7):** 
  Memory doesn't just save user and AI text messages—it also saves `ToolMessage` outputs in the state. For example, if the agent checks the weather for Mumbai and Bhopal in earlier turns, it remembers both tool results and can answer comparative follow-up questions later.

---

## 3. Complete Implementation (Chatbot with Memory & Continuous Loop)

Here is the complete code combining `MemorySaver`, `thread_id`, and a `while` loop for a continuous terminal-based chat session:

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = ChatOpenAI(model="gpt-4o-mini")


def chatbot(state: State):
    # Passes the entire conversation history to the LLM
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)


memory = MemorySaver()
graph = builder.compile(checkpointer=memory)


config = {"configurable": {"thread_id": "stark_session_1"}}


while True:
    user_input = input("Stark: ")
    
   
    if user_input.strip().lower() in ['exit', 'bye', 'close']:
        print("Jarvis: Session ended. Goodbye!")
        break
        
    
    res = graph.invoke({'messages': [("user", user_input)]}, config=config)
    
   
    print("Jarvis:", res['messages'][-1].content)
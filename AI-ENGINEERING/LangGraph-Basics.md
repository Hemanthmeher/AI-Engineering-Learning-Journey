# Section 28: Agents & LangGraph Foundations — Learning Notes

## 1. Introduction: Why Traditional Chains Aren't Enough
* **The Problem with Linear Chains:** Traditional LangChain workflows move strictly in a straight line: Step A $\rightarrow$ Step B $\rightarrow$ Step C. They are rigid and cannot adapt dynamically based on intermediate outputs.
* **The Need for Loops:** Real-world AI tasks (like fixing code, researching a topic, or fetching live stock prices) require **repetition and reasoning**. An agent needs to:
  1. **Think** about what to do.
  2. **Act** by executing a tool.
  3. **Observe** the result.
  4. **Repeat (Loop)** if the task isn't finished yet.

---

## 2. LangChain vs. LangGraph: Key Differences
* **LangChain:** Best for straightforward pipelines (e.g., prompt $\rightarrow$ LLM $\rightarrow$ output). It handles sequential data transformations smoothly.
* **LangGraph:** Built specifically for **stateful, multi-step agent workflows** that require **cycles and loops**. It allows agents to loop back, change direction, or wait for human input.

---

## 3. How Graph Theory Powers AI Agents
LangGraph uses concepts from **Graph Theory** to manage agent execution:
* **Nodes:** Represent the actions or steps (e.g., `call_llm` node, `run_tool` node).
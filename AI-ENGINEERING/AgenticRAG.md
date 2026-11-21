# Agentic RAG Foundations and Retrieval Pipeline

In this section, I moved from standard linear RAG pipelines to Agentic RAG architectures using LangGraph. Instead of blindly fetching documents and generating an answer in one pass, Agentic RAG introduces decision-making, document grading, query rewriting, and self-correction loops.

## 1. Why Traditional RAG Falls Short

Traditional RAG follows a fixed path: retrieve chunks -> stuff into prompt -> generate output. In practice, this breaks down in a few ways:

* It runs retrieval even when the user asks a simple greeting or general question that does not need external context.
* If the top-k retrieved chunks are noisy or irrelevant, the LLM still forces an answer or hallucinates.
* Poorly phrased user queries lead to weak vector matches with no fallback mechanism to rephrase and try again.

## 2. Agentic RAG Architecture

To fix this, I structured the retrieval workflow as a stateful graph where the LLM controls the flow:

1. **Agent Decision Node:** Evaluates the user query and decides whether to answer directly from parametric knowledge or invoke the retriever tool.
2. **Retriever Node (`ToolNode`):** Executes the vector search when requested by the agent.
3. **Document Grader:** Checks whether the retrieved chunks are actually relevant to the question.
4. **Query Rewriter:** If the documents fail the relevance check, the graph loops back, rewrites the user query for better semantic matching, and triggers retrieval again.
5. **Generator:** Produces the final grounded response once relevant context is confirmed.

## 3. Building the Retrieval Pipeline (Mini Project 9)

For the practical implementation, I built the core knowledge engine using external engineering articles (Anthropic's guide on building effective agents and AWS Bedrock AgentCore best practices).

### Document Loading and Flattening

I loaded the web pages using `WebBaseLoader`. Because loading multiple URLs returns a nested list of `Document` lists, I flattened the structure into a single list (`docs_list`) before splitting:

```python
from langchain_community.document_loaders import WebBaseLoader

urls = [
    "https://www.anthropic.com/engineering/building-effective-agents",
    "https://aws.amazon.com/blogs/machine-learning/ai-agents-in-enterprises-best-practices-with-amazon-bedrock-agentcore/",
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]
```

### Token-Based Chunking

Instead of splitting strictly by character count, I used `RecursiveCharacterTextSplitter.from_tiktoken_encoder` with `chunk_size=100` and `chunk_overlap=25`. Counting by tokens ensures each chunk stays strictly within model token budgets while preserving boundary context across overlaps.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=25
)
doc_splits = text_splitter.split_documents(docs_list)
```

### Vector Store, MMR Retrieval, and Tool Wrapping

I indexed the chunks into Chroma under a dedicated `collection_name` (`rag-chroma`) to isolate this dataset, then configured the retriever with Maximal Marginal Relevance (`mmr`) using `k=3` and `lambda_mult=0.6` so the results balance query relevance with diversity and avoid redundant chunks.

Finally, I wrapped the retriever with `create_retriever_tool`, writing a clear tool description so the LLM knows exactly when to trigger it, and converted the tool list into an executable `ToolNode` (`retriever_node`) ready to be wired into the LangGraph workflow.

```python
from langchain_community.vectorstores import Chroma
from langchain.tools.retriever import create_retriever_tool
from langgraph.prebuilt import ToolNode

vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=embeddings
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "lambda_mult": 0.6}
)

retriever_tool = create_retriever_tool(
    retriever,
    "retriever_web_page",
    "Search and return information from the indexed engineering blog posts."
)

tools = [retriever_tool]
retriever_node = ToolNode(tools)
```
# Section 30: Mastering Conditional Edges in LangGraph (My Learning Notes)Today, I explored one of the most powerful concepts in LangGraph: Conditional Edges. Until now, our workflows were linear (Node A $\rightarrow$ Node B $\rightarrow$ Node C). But real-world AI applications aren't linear—they need to make decisions (e.g., Is this question about our company data or general knowledge? Should we call a RAG pipeline or a standard LLM?). That's where conditional routing comes in!1. What is a Conditional Edge?Definition: A conditional edge acts like an if-else junction or a smart switch in our workflow graph.How it works: Instead of hardcoding a direct link from Node A to Node B, we pass the current state through a Router Function. Based on the output of that router, LangGraph dynamically decides which node to execute next.2. Core Components We Built in Mini Project 4To implement conditional routing, we broke down the architecture into 4 main parts:Step A: Classification Node (function_1)This node takes the user's query and classifies it into specific categories (e.g., NovaHarvest Technologies vs. Not Related) using Pydantic structured output parsing.Pythondef function_1(state: AgentState):

    print(*-> **FUNCTION** 1 (Classification) ->*)
    question = state[*messages*][-1]
    
    template = """
    Your task is to classify the given user query into one of the following categories: [NovaHarvest Technologies, Not Related].
    Only respond with the category name and nothing else.
    User query: {question}
    {format_instructions}
    """
    
    prompt = PromptTemplate(
    template=template,
    input_variables=[*question*],
    partial_variables={*format_instructions*: parser.get_format_instructions()},
    )
    
    chain = prompt | model | parser
    response = chain.invoke({*question*: question})
    
    # Returning the selected topic label into the state messages
    return {*messages*: [response.Topic]}
Step B: The Router Function (The Decision Maker)The router inspects the recent message in the state, checks its content, and returns a string destination label.Pythondef router(state: AgentState):
    print(*-> **ROUTER** ->*)
    last_message = state[*messages*][-1]
    
    # Check condition to decide path
    if *novaharvest technologies* in str(last_message).lower():
    return ***RAG** Call*
    else:
    return ***LLM** Call*
Step C: Execution Nodes (function_2 & function_3)Depending on what the router decides, the graph branches out:function_2 (**RAG** Call): Retrieves documents, formats context, and answers using proprietary company data.function_3 (**LLM** Call): Fallback path that answers using general world knowledge.Pythondef function_2(state: AgentState):
    print(*-> **RAG** Call Node ->*)
    question = state[*messages*][0] # Fetching original user query
    
    rag_chain = (
    {*context*: retriever | format_docs, *question*: RunnablePassthrough()}
    | prompt | model | StrOutputParser()
    )
    result = rag_chain.invoke(question)
    return {*messages*: [result]}

def function_3(state: AgentState):
    print(*-> **LLM** Call Node ->*)
    question = state[*messages*][0]
    
    complete_query = *Answer with real-world knowledge: * + str(question)
    response = model.invoke(complete_query)
    return {*messages*: [response.content]}
## Wiring the Graph with Conditional EdgesThis is where everything comes together. Instead of add_edge, we use add_conditional_edges and map the router's returned strings to actual node names!Pythonfrom langgraph.graph import StateGraph, END

# Initialize Graph

Gw = StateGraph(AgentState)

# 1. Register Nodes

Gw.add_node(*Classification*, function_1) Gw.add_node(*RAG*, function_2) Gw.add_node(*LLM*, function_3)

# 2. Set Entry Point

Gw.set_entry_point(*Classification*)

# 3. Add Conditional Routing

Gw.add_conditional_edges(
    *Classification*,  # Source node
    router,            # Router function
    {
    ***RAG** Call*: *RAG*,   # If router returns ***RAG** Call*, go to *RAG* node
    ***LLM** Call*: *LLM*    # If router returns ***LLM** Call*, go to *LLM* node
    }
)

# 4. Terminate branches

Gw.add_edge(*RAG*, **END**) Gw.add_edge(*LLM*, **END**)

# Compile

Graph = Gw.compile()
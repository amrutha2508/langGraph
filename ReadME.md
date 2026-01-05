## reACT Agent
1. Install following packages
    pip install langchain langchain_community langchain-google-genai python-dotenv
2. have these versions: pip install langchain==0.3.18 langchain-community==0.3.17 langchain-core==0.3.45 

## Structured LLM Output:
### Pydantic models:
1. pydantic is a python library that helps define data structures. Acts like blueprint for data
2. Uses pythons type hints(str,int) to enforce correct data types.
### In Langchain/LangGraph:
1. Define a class with the fields you need (name, capital, language)
2. Add descriptions to explain what each field means
3. Use with_structured_output() to tell the LLM to follow your format

## Reflection Agent
## 1. MessageGraph:
    1. a class tha langGraph provides that we can use to orchestrate the flow of messages between different nodes. if you just want to pass messages along between nodes, then go for MessageGraph.If the app requires complex state management, we have StateGraph
    2. MessageGraph maintains a list of messages and decides the flow of those messages between nodes.
        1. every node in messageGraph receives the full list of previous messages as input. 
        2. each node can append new messages to the list and return it.
        3. the updated message list is then passed to the next node.


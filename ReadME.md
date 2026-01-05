## reACT Agent with LangChain
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
### 1. MessageGraph:
    1. a class that langGraph provides that we can use to orchestrate the flow of messages between different nodes. if you just want to pass messages along between nodes, then go for MessageGraph.If the app requires complex state management, we have StateGraph
    2. MessageGraph maintains a list of messages and decides the flow of those messages between nodes.
        1. every node in messageGraph receives the full list of previous messages as input. 
        2. each node can append new messages to the list and return it.
        3. the updated message list is then passed to the next node.

## Reflexion Agent:
### 1. State in LangGRAPH: 
1. state is a way to maintain and track information as an AI system processes data.
2. a new state object is created at every node using the old state. states are immutable. 
3. STATE TRANSFORMATION : manual, annotated

## ReACT Agent with langGraph:
1. basic workflow of ReACT: **think -> action -> action_input -> tools execution -> observe** 
2. LangChains initialize_agent is made of create_react_agent + AgentExecutor

3. create_react_Agent returns : AgentAction or AgentFinish(None in initial instance) class as output
AgentAction(
    tool="search",
    tool_input="LangGraph reducers",
    log="Action: search\nAction Input: LangGraph reducers"
)
AgentAction(
    tool="search",
    tool_input="LangGraph reducers",
    log="Action: search\nAction Input: LangGraph reducers"
)

### Full ReAct workflow (step-by-step)
Let’s walk through a real run.
1. User input : "What is the capital of France?"
2. Step 1: Agent plans
    LLM sees:
    User question
    Tool descriptions
    Previous steps (none yet)
3. LLM outputs:
    Thought: I should look this up.
    Action: search
    Action Input: "capital of France"
4. 🔁 Parsed into AgentAction
    AgentAction(
        tool="search",
        tool_input="capital of France",
        log="Thought: ... Action: search ..."
    )
5. 🛠 : Tool execution
    AgentExecutor runs:
    observation = search("capital of France")
    Result:
    "Paris"
6. 🧠 : Observation is appended
    intermediate_steps = [
        (AgentAction(...), "Paris")
    ]
    This becomes part of the next prompt.
7. 🧠 : Agent plans again
    LLM now sees:
    Thought: I should look this up.
    Action: search
    Action Input: capital of France
    Observation: Paris
8. LLM outputs:
    Thought: I now know the answer.
    Final Answer: The capital of France is Paris.
9. 🏁 Parsed into AgentFinish
    AgentFinish(
        return_values={"output": "The capital of France is Paris."},
        log="Final Answer: ..."
    )
10. Execution stops
    AgentExecutor sees AgentFinish → returns output to user.

--> Where tools fit in (important) Tools are never called by the LLM directly.
Flow is always: LLM → AgentAction → Executor → Tool → Observation → LLMLLM decides, executor acts.

    
### ex:
python 5_react_agent/react_graph.py
    agentOutcome: tool='tavily_search_results_json' tool_input='latest SpaceX launch date' log='I need to find the date of the latest SpaceX launch and compare it with the current date.\nAction: tavily_search_results_json\nAction Input: "latest SpaceX launch date"'
    <class 'langchain_core.agents.AgentAction'>
    agentOutcome: tool='tavily_search_results_json' tool_input='most recent SpaceX launch date' log='The search results seem to be showing future launch dates, instead of the most recent one. I need to refine my search.\nAction: tavily_search_results_json\nAction Input: "most recent SpaceX launch date"'
    <class 'langchain_core.agents.AgentAction'>
    agentOutcome: tool='get_system_time' tool_input="'%Y-%m-%d'" log="The most recent launch date found is January 4. Now I need to calculate how many days have passed since that date.\nAction: get_system_time\nAction Input: '%Y-%m-%d'"
    <class 'langchain_core.agents.AgentAction'>
    agentOutcome: return_values={'output': 'The latest SpaceX launch was 1 day ago.'} log='The current date is January 5, 2026, and the recent launch was on January 4, 2026. Thus, one day has passed since the latest SpaceX launch.\nFinal Answer: The latest SpaceX launch was 1 day ago.'
    <class 'langchain_core.agents.AgentFinish'>
    The latest SpaceX launch was 1 day ago. final result




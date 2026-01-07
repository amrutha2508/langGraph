from typing import TypedDict, Annotated
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END, add_messages
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
llm = ChatGroq(model="llama-3.1-8b-instant")

class State(TypedDict):
    messages: Annotated[list, add_messages]

GENERATE_POST = "generate_post"
GET_REVIEW_DECISION = "get_review_decision"
POST = "post"
COLLECT_FEEDBACK = "collect_feedback"

def generate_post(state: State):
    return {
        "messages": [llm.invoke(state["messages"])]
    }
def get_review_decision(state: State):
    post_content = state["messages"][-1].content

    print("Current linkedin post:")
    print(post_content)
    print("\n")
    decision = input("Post to linkedIn: (yes/no): ")
    if decision.lower() =="yes":
        return POST
    else:
        return COLLECT_FEEDBACK


def post(state: State):  
    final_post = state["messages"][-1].content  
    print("\n📢 Final LinkedIn Post:\n")
    print(final_post)
    print("\n✅ Post has been approved and is now live on LinkedIn!")

def collect_feedback(state: State):  
    feedback = input("How can I improve this post?")
    return {
        "messages": [HumanMessage(content=feedback)]
    }

graph = StateGraph(State)

graph.add_node(GENERATE_POST,generate_post)
graph.add_node(COLLECT_FEEDBACK,collect_feedback)
graph.set_entry_point(GENERATE_POST)
graph.add_node(POST,post)

graph.add_edge(COLLECT_FEEDBACK,GENERATE_POST)
graph.add_conditional_edges(GENERATE_POST,get_review_decision)
graph.add_edge(POST,END)

app = graph.compile()

response = app.invoke({
    "messages": [HumanMessage(content="Write me a LinkedIn post on AI Agents taking over content creation")]
})

print(response)
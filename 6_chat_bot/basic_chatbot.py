from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, add_messages, END
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: BasicChatState):
    return {
        "messages": [llm.invoke(state["messages"])]
    }

graph = StateGraph(BasicChatState)

graph.add_node("chatbot", chatbot)
graph.add_edge("chatbot",END)
graph.set_entry_point("chatbot")

app = graph.compile()

while True:
    user_input = input("User: ")
    if (user_input in ["exit","end"]):
        break
    else:
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        })
        print(result)


# python 6_chat_bot/basic_chatbot.py
# User: what's the weather in bangalore?
# {'messages': [HumanMessage(content="what's the weather in bangalore?", additional_kwargs={}, response_metadata={}, id='1a79770d-2363-4593-98ef-81c27311d202'), AIMessage(content='However, I\'m a large language model, I don\'t have real-time access to current weather conditions. But I can suggest some ways for you to find out the current weather in Bangalore.\n\nYou can check the following websites or apps for the current weather in Bangalore:\n\n1. **AccuWeather**: accuweather.com\n2. **Weather.com**: weather.com\n3. **India Meteorological Department**: imd.gov.in\n4. **Dark Sky (now The Weather Channel)**: apps.apple.com/us/app/dark-sky/id714085922\n5. **Google Search**: simply type "weather in Bangalore" and you\'ll get the current weather conditions.\n\nThat being said, Bangalore typically experiences a climate with three main seasons:\n\n1. **Summer (March to May)**: Hot and dry, with temperatures ranging from 22°C to 35°C (72°F to 95°F).\n2. **Monsoon (June to September)**: Humid and rainy, with temperatures ranging from 18°C to 28°C (64°F to 82°F).\n3. **Winter (October to February)**: Mild and pleasant, with temperatures ranging from 10°C to 22°C (50°F to 72°F).\n\nPlease note that these are general temperature ranges, and actual weather conditions can vary from year to year.\n\nIf you want to know the current weather in Bangalore, I recommend checking the websites or apps mentioned above.', additional_kwargs={}, response_metadata={'token_usage': {'completion_tokens': 293, 'prompt_tokens': 43, 'total_tokens': 336, 'completion_time': 0.369027453, 'prompt_time': 0.002831359, 'queue_time': 0.00551351, 'total_time': 0.371858812}, 'model_name': 'llama-3.1-8b-instant', 'system_fingerprint': 'fp_6c980774ec', 'finish_reason': 'stop', 'logprobs': None}, id='run-d700ade8-4180-427e-8dc0-3c028a27c909-0', usage_metadata={'input_tokens': 43, 'output_tokens': 293, 'total_tokens': 336})]}
# User: end
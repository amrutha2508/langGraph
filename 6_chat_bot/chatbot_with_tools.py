from typing import TypedDict, Annotated
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END, add_messages
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode

load_dotenv()

class BasicChatBot(TypedDict):
    messages : Annotated[list, add_messages]

search_tool = TavilySearchResults(max_results=2)

tools = [search_tool]

llm = ChatGroq(model="llama-3.1-8b-instant")
llm_with_tools = llm.bind_tools(tools = tools)

def chatbot(state:BasicChatBot):
    return {
        "messages":[llm_with_tools.invoke(state["messages"])]
    }

def tools_router(state: BasicChatBot):
    last_message = state["messages"][-1]
    if (hasattr(last_message, "tool_calls") and len(last_message.tool_calls)>0):
        return "tool_node"
    else:
        return END
    
tool_node = ToolNode(tools=tools)

graph = StateGraph(BasicChatBot)

graph.add_node("chatbot",chatbot)
graph.add_node("tool_node",tool_node)
graph.set_entry_point("chatbot")

graph.add_edge("tool_node","chatbot")
graph.add_conditional_edges("chatbot",tools_router)

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


# User: what's the weather in bangalore?
# {'messages': [HumanMessage(content="what's the weather in bangalore?", additional_kwargs={}, response_metadata={}, id='265198f8-cf76-4706-95c0-8c5207ae1183'), AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'ds1gea66j', 'function': {'arguments': '{"query":"bangalore weather"}', 'name': 'tavily_search_results_json'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 21, 'prompt_tokens': 286, 'total_tokens': 307, 'completion_time': 0.035255272, 'prompt_time': 0.026968024, 'queue_time': 0.009508113, 'total_time': 0.062223296}, 'model_name': 'llama-3.1-8b-instant', 'system_fingerprint': 'fp_6c980774ec', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-9f672d80-110e-4d41-8bbe-61460680d79e-0', tool_calls=[{'name': 'tavily_search_results_json', 'args': {'query': 'bangalore weather'}, 'id': 'ds1gea66j', 'type': 'tool_call'}], usage_metadata={'input_tokens': 286, 'output_tokens': 21, 'total_tokens': 307}), ToolMessage(content='[{"url": "https://www.weather25.com/asia/india/karnataka/bangalore?page=month&month=January", "content": "| June | 30° / 21° | 10 | 20 | 0 | 183 mm | Ok | Bangalore in June |\\n| July | 28° / 20° | 9 | 22 | 0 | 141 mm | Good | Bangalore in July |\\n| August | 28° / 20° | 14 | 17 | 0 | 251 mm | Good | Bangalore in August |\\n| September | 28° / 20° | 15 | 15 | 0 | 304 mm | Good | Bangalore in September |\\n| October | 28° / 19° | 13 | 18 | 0 | 297 mm | Good | Bangalore in October |\\n| November | 27° / 18° | 8 | 22 | 0 | 158 mm | Good | Bangalore in November | [...] United States England Australia Canada\\n\\n°F °C\\n\\nWeather in January 2026\\n\\n1. Home\\n2. Asia\\n3. India\\n4. Karnataka\\n5. Bangalore\\n6. January\\n\\nLocation was added to My Locations\\n\\nLocation was removed from My Locations\\n\\n# Bangalore weather in January 2026\\n\\nClick on a day for an hourly weather forecast\\n\\nDec 19\\n\\n0 mm\\n\\n26° / 15°Dec 20\\n\\n0 mm\\n\\n26° / 14°Dec 21\\n\\n0 mm\\n\\n25° / 14°Monday\\n\\nDec 22\\n\\n0 mm\\n\\n26° / 14°Tuesday\\n\\nDec 23\\n\\n0 mm\\n\\n26° / 14°Wednesday\\n\\nDec 24\\n\\n0 mm\\n\\n26° / 14°Thursday\\n\\nDec 25\\n\\n0 mm\\n\\n26° / 14°Friday"}, {"url": "https://www.metcheck.com/WEATHER/dayforecast.asp?location=Bengaluru&locationID=2410798&lat=12.97194&lon=77.59369&dateFor=06/01/2026", "content": "◄ Mon\\n 16 Days ▼\\n Wed ►\\n\\n  \\n |  |  |\\n --- |\\n| Model/Location Information |  |\\n\\n|  |  |\\n --- |\\n| Models Used | MODELSUPDATED |\\n| Forecast Generated | 06 January 2026 06:53 GMT |\\n| Latitude | 12.97194N |\\n| Longitude | 77.59369E |\\n| Moon | Moon Rise/Set Times ► |\\n| Sun | Sun Rise/Set Times ► |\\n\\n|  |  |\\n --- |\\n| Help & Information |  |\\n\\n|  | [...] | Tuesday 6 January☀ ▲ 6:13    17:36  ▼ ☼ |\\n| |  |  |  |  |  |  |  |  |  |  |  |  |  |  ---  ---  ---  ---  ---  ---  | ▲ | 12:00 | 13:00 | 14:00 | 15:00 | 16:00 | 17:00 | 18:00 | 19:00 | 20:00 | 21:00 | 22:00 | 23:00 | |  |  |  |  |  |  |  |  |  |  |  |  |  | |\\n| Time | Temp | Feels | RainRisk | Amount | Cloud | Dir | Speed | Gust | RH | UV | Weather |\\n| 12:00 | 24 °c | 26 °c | 0% | 0.0mm | 18% | 6mph | 7mph | 43% | 8 |\\n| 13:00 | 25 °c | 27 °c | 0% | 0.0mm | 24% | 6mph | 7mph | 41% | 7 | [...] | 21:00 | 19 °c | 21 °c | 0% | 0.0mm | 44% | 4mph | 15mph | 55% | 0 |\\n| 22:00 | 18 °c | 19 °c | 0% | 0.0mm | 88% | 6mph | 16mph | 56% | 0 |\\n| 23:00 | 17 °c | 18 °c | 0% | 0.0mm | 68% | 4mph | 8mph | 63% | 0 |"}]', name='tavily_search_results_json', id='cac4ae30-4b6c-4b52-b638-663e4fba6ec9', tool_call_id='ds1gea66j', artifact={'query': 'bangalore weather', 'follow_up_questions': None, 'answer': None, 'images': [], 'results': [{'url': 'https://www.weather25.com/asia/india/karnataka/bangalore?page=month&month=January', 'title': 'Bangalore weather in January 2026 - Weather25.com', 'content': '| June | 30° / 21° | 10 | 20 | 0 | 183 mm | Ok | Bangalore in June |\n| July | 28° / 20° | 9 | 22 | 0 | 141 mm | Good | Bangalore in July |\n| August | 28° / 20° | 14 | 17 | 0 | 251 mm | Good | Bangalore in August |\n| September | 28° / 20° | 15 | 15 | 0 | 304 mm | Good | Bangalore in September |\n| October | 28° / 19° | 13 | 18 | 0 | 297 mm | Good | Bangalore in October |\n| November | 27° / 18° | 8 | 22 | 0 | 158 mm | Good | Bangalore in November | [...] United States England Australia Canada\n\n°F °C\n\nWeather in January 2026\n\n1. Home\n2. Asia\n3. India\n4. Karnataka\n5. Bangalore\n6. January\n\nLocation was added to My Locations\n\nLocation was removed from My Locations\n\n# Bangalore weather in January 2026\n\nClick on a day for an hourly weather forecast\n\nDec 19\n\n0 mm\n\n26° / 15°Dec 20\n\n0 mm\n\n26° / 14°Dec 21\n\n0 mm\n\n25° / 14°Monday\n\nDec 22\n\n0 mm\n\n26° / 14°Tuesday\n\nDec 23\n\n0 mm\n\n26° / 14°Wednesday\n\nDec 24\n\n0 mm\n\n26° / 14°Thursday\n\nDec 25\n\n0 mm\n\n26° / 14°Friday', 'score': 0.86024034, 'raw_content': None}, {'url': 'https://www.metcheck.com/WEATHER/dayforecast.asp?location=Bengaluru&locationID=2410798&lat=12.97194&lon=77.59369&dateFor=06/01/2026', 'title': 'Weather Forecast for Bengaluru for Tuesday 6 January', 'content': '◄ Mon\n 16 Days ▼\n Wed ►\n\n  \n |  |  |\n --- |\n| Model/Location Information |  |\n\n|  |  |\n --- |\n| Models Used | MODELSUPDATED |\n| Forecast Generated | 06 January 2026 06:53 GMT |\n| Latitude | 12.97194N |\n| Longitude | 77.59369E |\n| Moon | Moon Rise/Set Times ► |\n| Sun | Sun Rise/Set Times ► |\n\n|  |  |\n --- |\n| Help & Information |  |\n\n|  | [...] | Tuesday 6 January☀ ▲ 6:13    17:36  ▼ ☼ |\n| |  |  |  |  |  |  |  |  |  |  |  |  |  |  ---  ---  ---  ---  ---  ---  | ▲ | 12:00 | 13:00 | 14:00 | 15:00 | 16:00 | 17:00 | 18:00 | 19:00 | 20:00 | 21:00 | 22:00 | 23:00 | |  |  |  |  |  |  |  |  |  |  |  |  |  | |\n| Time | Temp | Feels | RainRisk | Amount | Cloud | Dir | Speed | Gust | RH | UV | Weather |\n| 12:00 | 24 °c | 26 °c | 0% | 0.0mm | 18% | 6mph | 7mph | 43% | 8 |\n| 13:00 | 25 °c | 27 °c | 0% | 0.0mm | 24% | 6mph | 7mph | 41% | 7 | [...] | 21:00 | 19 °c | 21 °c | 0% | 0.0mm | 44% | 4mph | 15mph | 55% | 0 |\n| 22:00 | 18 °c | 19 °c | 0% | 0.0mm | 88% | 6mph | 16mph | 56% | 0 |\n| 23:00 | 17 °c | 18 °c | 0% | 0.0mm | 68% | 4mph | 8mph | 63% | 0 |', 'score': 0.8266142, 'raw_content': None}], 'response_time': 3.97, 'request_id': '8c70d5f1-4516-4657-af55-948c8e286123'}), AIMessage(content='The current weather in Bangalore is 24°C with a feels like temperature of 26°C. There is a 0% chance of rain and the cloud cover is at 18%. The wind speed is 6mph and the gust speed is 7mph. The relative humidity is 43% and the UV index is 8.', additional_kwargs={}, response_metadata={'token_usage': {'completion_tokens': 69, 'prompt_tokens': 1346, 'total_tokens': 1415, 'completion_time': 0.109130809, 'prompt_time': 0.10545979, 'queue_time': 0.009537624, 'total_time': 0.214590599}, 'model_name': 'llama-3.1-8b-instant', 'system_fingerprint': 'fp_9ca2574dca', 'finish_reason': 'stop', 'logprobs': None}, id='run-c1789cfb-2ff7-4c51-b2a9-fe01966103d0-0', usage_metadata={'input_tokens': 1346, 'output_tokens': 69, 'total_tokens': 1415})]}
# User: end
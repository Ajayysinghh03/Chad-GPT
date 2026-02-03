from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode , tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool, tool
from dotenv import load_dotenv
import sqlite3
import requests

load_dotenv()


### ********************TOOLS DEFINITION SECTION******************** ###
search_tool = DuckDuckGoSearchRun(region="in", safesearch="Moderate")

@tool
def calculator(first_num:float, second_num:float, operation:str) -> dict:
    """Here is a simple calculator which can perform basic arithmatic operations but keep in mind to follow BODMAS rules"""
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed."}
            result = first_num / second_num
        else:
            return {"error": "Invalid operation. Please use add, sub, mul, or div."}
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}
    
@tool
def get_stock_price(symbol: str) -> dict:
    """Get the current stock price for a given symbol using a public API."""
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey=55W3PSBIJOH81THN'
    r = requests.get(url)
    return r.json()



tools = [search_tool, calculator, get_stock_price]



llm = ChatGroq(
    model="llama-3.3-70b-versatile", temperature=0.8
)

llm = llm.bind_tools(tools)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    """LLM node that may answer the question directly and can call tools if needed."""
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": response}

tool_node = ToolNode(tools)

conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)  #in memory saver is for ram base checkpointing but we want database persistence


### ******************Graph definition ****************** ###
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)


graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

def rerieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)
from langgraph.graph import StateGraph , START , END
from typing import TypedDict ,Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel , Field
from langchain_core.messages import BaseMessage 
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
# from langgraph.checkpoint.memory import MemorySaver
# now we are using sql database saver
from langchain_core.messages import BaseMessage , HumanMessage
from __future__ import annotations

from langgraph.checkpoint.sqlite import SqliteSaver 
import os
import sqlite3
import requests
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool
import asyncio

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", api_key=os.getenv('GOOGLE_API_KEY'))
llm = model

search_tool = DuckDuckGoSearchResults(region='us-en')

@tool
def calulator(first_num : float , second_num : float , operation : str) ->dict:
    '''
    This is a calculator tool that takes in two numbers and an operation and returns the result of the operation.
    '''
    try:
        if operation == 'add':
            return first_num + second_num
        elif operation == 'subtract':
            return first_num - second_num
        elif operation == 'multiply':
            return first_num * second_num
        elif operation == 'divide':
            return first_num / second_num    
    except Exception as e:
        return f"Error: {e}"    


@tool
def getStockPrices(symbol : str) ->dict:
    '''
    This is a tool that takes in a stock symbol and returns the current price of the stock.
    '''
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey=WA2WYAFCSUGVABNP"
    r = requests.get(url)
    return r.json()

tools = [search_tool , getStockPrices , calulator]

llm_with_tools = llm.bind_tools(tools)

class ChatState(TypedDict):
    # base message is the initial message that the user sends to the chatbot, and it is required.
    messages : Annotated[list[BaseMessage] ,add_messages] 

def build_graph():
    async def chat_node(state:ChatState) -> ChatState:
    
    # take user query from the state
        messages = state['messages']

        # get response from the model
        # without tools
        # response = llm.invoke(messages)
        # with tools
        response = await llm_with_tools.ainvoke(messages)
        
        # add response to the state
        return {'messages': [response]}

    graph = StateGraph(ChatState)
    tool_node = ToolNode(tools)

    graph.add_node('chat_node' , chat_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START , 'chat_node')
    graph.add_conditional_edges("chat_node",tools_condition)
    graph.add_edge('tools', 'chat_node')

    chatbot = graph.compile()
    return chatbot

async def main():
    chatbot = build_graph()
    result = await res = chatbot.ainvoke({'messages': [HumanMessage(content=user_input)]} , config=CONFIG)
    response = res["messages"][-1]


if __name__ == "__main__":
    asyncio.run(main())
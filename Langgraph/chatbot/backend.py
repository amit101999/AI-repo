from langgraph.graph import StateGraph , START , END
from typing import TypedDict ,Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel , Field
from langchain_core.messages import BaseMessage 
import os
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver


load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", api_key=os.getenv('API_KEY'))

class ChatState(TypedDict):
    # base message is the initial message that the user sends to the chatbot, and it is required.
    messages : Annotated[list[BaseMessage] ,add_messages] 

llm = model

def chat_node(state:ChatState) -> ChatState:
    
    # take user query from the state
    messages = state['messages']

    # get response from the model
    response = llm.invoke(messages)
    
    # add response to the state
    return {'messages': [response]}

checkpointer = MemorySaver()
graph = StateGraph(ChatState)

graph.add_node('chat_node' , chat_node)


graph.add_edge(START , 'chat_node')
graph.add_edge('chat_node' , END)

chatbot = graph.compile(checkpointer=checkpointer)

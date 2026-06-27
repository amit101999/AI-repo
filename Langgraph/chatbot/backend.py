from __future__ import annotations
from langgraph.graph import StateGraph , START , END
from typing import  Annotated, Any, Dict, Optional, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from pydantic import BaseModel , Field
from langchain_core.messages import BaseMessage , SystemMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
# from langgraph.checkpoint.memory import MemorySaver
# now we are using sql database saver
from langgraph.checkpoint.sqlite import SqliteSaver
import os
import sqlite3
import tempfile
import requests
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", api_key=os.getenv('GOOGLE_API_KEY'))
llm = model
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# -------------------
# 2. PDF retriever store (per thread)
# -------------------
_THREAD_RETRIEVERS: Dict[str, Any] = {}
_THREAD_METADATA: Dict[str, dict] = {}

def _get_retriever(thread_id: Optional[str]):
    """Fetch the retriever for a thread if available."""
    if thread_id and thread_id in _THREAD_RETRIEVERS:
        return _THREAD_RETRIEVERS[thread_id]
    return None

def ingest_pdf(file_bytes: bytes, thread_id: str, filename: Optional[str] = None) -> dict:
    """
    Build a FAISS retriever for the uploaded PDF and store it for the thread.

    Returns a summary dict that can be surfaced in the UI.
    """
    if not file_bytes:
        raise ValueError("No bytes received for ingestion.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file_bytes)
        temp_path = temp_file.name

    try:
        loader = PyPDFLoader(temp_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
        )
        chunks = splitter.split_documents(docs)

        vector_store = FAISS.from_documents(chunks, embeddings)
        retriever = vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": 4}
        )

        _THREAD_RETRIEVERS[str(thread_id)] = retriever
        _THREAD_METADATA[str(thread_id)] = {
            "filename": filename or os.path.basename(temp_path),
            "documents": len(docs),
            "chunks": len(chunks),
        }

        return {
            "filename": filename or os.path.basename(temp_path),
            "documents": len(docs),
            "chunks": len(chunks),
        }
    finally:
        # The FAISS store keeps copies of the text, so the temp file is safe to remove.
        try:
            os.remove(temp_path)
        except OSError:
            pass

@tool
def rag_tool(query: str, thread_id: str) -> str:
    '''
    Answer questions about the PDF uploaded for this chat. Pass the user's
    question as `query` and the current `thread_id`. Returns the most relevant
    passages from the document.
    '''
    retriever = _get_retriever(thread_id)
    if retriever is None:
        return "No PDF has been uploaded for this conversation yet."
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant passages were found in the uploaded PDF."
    return "\n\n".join(d.page_content for d in docs)


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

tools = [search_tool , getStockPrices , calulator , rag_tool]

llm_with_tools = llm.bind_tools(tools)

class ChatState(TypedDict):
    # base message is the initial message that the user sends to the chatbot, and it is required.
    messages : Annotated[list[BaseMessage] ,add_messages] 

def chat_node(state: ChatState, config=None) -> ChatState:
    """LLM node that may answer or request a tool call."""
    thread_id = None
    if config and isinstance(config, dict):
        thread_id = config.get("configurable", {}).get("thread_id")

    system_message = SystemMessage(
        content=(
            "You are a helpful assistant. For questions about the uploaded PDF, call "
            "the `rag_tool` and include the thread_id "
            f"`{thread_id}`. You can also use the web search, stock price, and "
            "calculator tools when helpful. If no document is available, ask the user "
            "to upload a PDF."
        )
    )

    messages = [system_message, *state["messages"]]
    response = llm_with_tools.invoke(messages, config=config)
    return {"messages": [response]}

# checkpointer = MemorySaver()
# we are using sql database saver instead of memory saver, so that the message history can be persisted even after the server restarts.
conn = sqlite3.connect(database="chat_history.db" , check_same_thread=False)
# checksame_thread is set to False to allow multiple threads to access the database, which is required for the streaming response to work properly.
checkpointer = SqliteSaver(conn=conn)
graph = StateGraph(ChatState)

tool_node = ToolNode(tools)

graph.add_node('chat_node' , chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START , 'chat_node')
graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge('tools', 'chat_node')

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    # mean we want all checkpoints that means we have said None
    for checkpoints in checkpointer.list(None):
        all_threads.add(checkpoints.config['configurable']['thread_id'])
    return list(all_threads)



def thread_has_document(thread_id: str) -> bool:
    return str(thread_id) in _THREAD_RETRIEVERS


def thread_document_metadata(thread_id: str) -> dict:
    return _THREAD_METADATA.get(str(thread_id), {})

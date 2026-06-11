import streamlit as st
from  backend import chatbot
from langchain_core.messages import BaseMessage , HumanMessage
import uuid


# ----------------------------UTILITY FUNCTIONS----------------------------

def generate_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_convsersation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get("messages", [])



message_history = []
#  ---------------------- SESSION SETUP-----------------------------------------------------

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_thread(st.session_state['thread_id'])


# ----------------------------------SIDE BAR UI ----------------------------------------------

st.sidebar.title("MyCHAT")

if st.sidebar.button("New Chat"):
        reset_chat()

st.sidebar.header("My Chats")

for thread in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread)):
        st.session_state['thread_id'] = thread
        messages = load_convsersation(thread)

        temp_msg =[]

        for msg in messages:

           role = "user" if isinstance(msg, HumanMessage) else "assistant"

           content = msg.content

           if isinstance(content, list):
               content = content[0]["text"] if len(content) > 0 else ""

           temp_msg.append({
          "role": role,
          "content": content
        })

        st.session_state['message_history'] = temp_msg





# ---------------------------------- CHAT UI ----------------------------------------------


# loading the message history from the memory saver
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])



        
 # for streaming response, we will yield the response as it comes in, and update the message history in the session state
def stream_response():
    CONFIG = { 'configurable' : { 'thread_id': st.session_state['thread_id'] } }

    for msg_chunk, metadata in chatbot.stream(
        {"messages": [HumanMessage(content=user_input)]},
        config=CONFIG,
        stream_mode="messages"
    ):
        content = msg_chunk.content

        if isinstance(content, list):
            if len(content) > 0:
                yield content[0]["text"]
        else:
            yield content

user_input = st.chat_input("type here to continue the conversation...")

if user_input:
    
    # first add to the message history
     st.session_state['message_history'].append({'role': 'user', 'content': user_input})

     with st.chat_message("user"):
          st.text(user_input)


    # without streaming
    #  res = chatbot.invoke({'messages': [HumanMessage(content=user_input)]} , config=CONFIG)
    #  response = res["messages"][-1]
    #  if isinstance(response.content, list):
    #         ai_msg = response.content[0]["text"]
    #  else:
    #         ai_msg = response.content

    #     # get response from the model
    #  st.session_state['message_history'].append({'role': 'assistant', 'content': ai_msg})
    #  with st.chat_message("assistant"):
    #       st.text(ai_msg)

    # with streaming
     with st.chat_message("assistant"):
        ai_msg = st.write_stream(stream_response)

        st.session_state["message_history"].append(
            {
                "role": "assistant",
                "content": ai_msg
            }
)




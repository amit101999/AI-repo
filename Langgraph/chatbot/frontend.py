import streamlit as st
from backend import chatbot, retrieve_all_threads, ingest_pdf
import uuid
from langchain_core.messages import HumanMessage

# ----------------------------UTILITY FUNCTIONS----------------------------

def generate_thread_id():
    return str(uuid.uuid4())

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['message_history'] = []
    st.session_state['thread_docs'] = {}

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get("messages", [])


# ---------------------- SESSION SETUP -----------------------------------

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

if 'thread_docs' not in st.session_state:
    st.session_state['thread_docs'] = {}

add_thread(st.session_state['thread_id'])

thread_key = st.session_state['thread_id']
thread_docs = st.session_state['thread_docs']


# ---------------------------------- SIDEBAR UI --------------------------

st.sidebar.title("LangGraph PDF Chatbot")
st.sidebar.markdown(f"**Thread ID:** `{thread_key}`")

if st.sidebar.button("New Chat", use_container_width=True):
    reset_chat()
    st.rerun()

# ----- PDF upload -----
uploaded_pdf = st.sidebar.file_uploader("Upload a PDF for this chat", type=["pdf"])
if uploaded_pdf:
    if uploaded_pdf.name in thread_docs:
        st.sidebar.info(f"`{uploaded_pdf.name}` already processed for this chat.")
    else:
        with st.sidebar.status("Indexing PDF…", expanded=True) as status_box:
            summary = ingest_pdf(
                uploaded_pdf.getvalue(),
                thread_id=thread_key,
                filename=uploaded_pdf.name,
            )
            thread_docs[uploaded_pdf.name] = summary
            status_box.update(label="✅ PDF indexed", state="complete", expanded=False)

if thread_docs:
    latest_doc = list(thread_docs.values())[-1]
    st.sidebar.success(
        f"Using `{latest_doc.get('filename')}` "
        f"({latest_doc.get('chunks')} chunks from {latest_doc.get('documents')} pages)"
    )
else:
    st.sidebar.info("No PDF indexed yet.")

# ----- Past conversations -----
st.sidebar.subheader("Past conversations")
if not st.session_state['chat_threads']:
    st.sidebar.write("No past conversations yet.")
else:
    for thread_id in st.session_state['chat_threads']:
        if st.sidebar.button(str(thread_id), key=f"side-thread-{thread_id}"):
            st.session_state['thread_id'] = thread_id
            messages = load_conversation(thread_id)

            temp_msg = []
            for msg in messages:
                role = "user" if isinstance(msg, HumanMessage) else "assistant"
                content = msg.content
                if isinstance(content, list):
                    content = content[0]["text"] if len(content) > 0 else ""
                temp_msg.append({"role": role, "content": content})

            st.session_state['message_history'] = temp_msg
            st.rerun()


# ---------------------------------- CHAT UI -----------------------------

# loading the message history from the checkpointer
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


# for streaming response, we yield the response as it comes in
def stream_response(user_input):
    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    for msg_chunk, metadata in chatbot.stream(
        {"messages": [HumanMessage(content=user_input)]},
        config=CONFIG,
        stream_mode="messages",
    ):
        content = msg_chunk.content
        if isinstance(content, list):
            if len(content) > 0 and isinstance(content[0], dict):
                yield content[0].get("text", "")
        elif content:
            yield content


user_input = st.chat_input("type here to continue the conversation...")

if user_input:
    # first add to the message history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message("user"):
        st.text(user_input)

    # with streaming
    with st.chat_message("assistant"):
        ai_msg = st.write_stream(stream_response(user_input))

    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_msg}
    )

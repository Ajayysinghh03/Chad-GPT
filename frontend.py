import streamlit as st
from backend import chatbot, rerieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import uuid

# ***************  UTILITY FUNCTIONS *****************
def generate_thread_id():
    tid = uuid.uuid4()
    return tid

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["history"] = []

def add_thread(thread_id):
    if st.session_state["chat_threads"] is None:
        st.session_state["chat_threads"] = []
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config = {"configurable":{"thread_id": thread_id}})
    if state.values:
        return state.values.get("messages", [])
    return []
    
        
        
st.set_page_config(
    page_title="Srii",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Srii")


# *************** SESSION SETUP ******************
if "history" not in st.session_state:
    st.session_state["history"] = [{"role": "ai", "content": "Hello! How can I assist you today?"}]

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = rerieve_all_threads()

add_thread(st.session_state["thread_id"])

CONFIG = {"configurable":{"thread_id": st.session_state["thread_id"]}}

# *************** SIDEBAR UI *****************
st.sidebar.title("Srii's Tools 🤖")
with st.sidebar:
    if st.button("🧹 Clear Chat"):
        st.session_state.history = []
        
    with st.expander("About Srii"):
        st.markdown("""
            - Siri ❌ Srii ✅
            - Made by Ajay
            - Using LangGraph 
            """)
    st.set_page_config(
    page_title="Srii",
    page_icon="🤖",
    layout="centered"
    )
if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Chats")

for thread_id in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"] = thread_id
        messages = load_conversation(thread_id)
        temp_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                temp_messages.append({"role": "user", "content": message.content})
            else:
                temp_messages.append({"role": "ai", "content": message.content})
        st.session_state["history"] = temp_messages




for message in st.session_state["history"]:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


user_input = st.chat_input("Type your message here...")

if user_input:
    st.toast("Message sent 🚀")

    st.session_state["history"].append({"role": "user", "content": user_input})
    with st.chat_message("human"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]}, config=CONFIG,
                stream_mode="messages"
            )
        )
    st.session_state["history"].append({"role": "assistant", "content": ai_message})


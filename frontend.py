import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


# *************** SIDEBAR UI *****************
st.sidebar.title("Srii's Tools 🤖")
with st.sidebar:
    
    if st.button("🧹 Clear Chat"):
        st.session_state.history = []
        st.session_state["thread_id"] += 1
        st.rerun()
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
st.sidebar.button("New Chat")
st.sidebar.header("My Chats")
        
        
st.set_page_config(
    page_title="Srii",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Srii")

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = 1

CONFIG = {"configurable":{"thread_id": st.session_state["thread_id"]}}

if "history" not in st.session_state:
    st.session_state["history"] = [{"role": "ai", "content": "Hello! How can I assist you today?"}]

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


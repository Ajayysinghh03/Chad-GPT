import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

with st.sidebar:
    st.header("Configurations")
    if st.button("🧹 Clear Chat"):
        st.session_state.history = []
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
        
        
st.set_page_config(
    page_title="Srii",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Srii")

CONFIG = {"configurable":{"thread_id": 1}}

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

    response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]}, config=CONFIG)
    ai_message = response["messages"][-1].content
    st.session_state["history"].append({"role": "ai", "content": ai_message})
    with st.chat_message("ai"):
        st.markdown(ai_message)


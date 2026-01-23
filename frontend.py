import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

CONFIG = {"configurable":{"thread_id": 1}}

if "history" not in st.session_state:
    st.session_state["history"] = [{"role": "ai", "content": "Hello! How can I assist you today?"}]

for message in st.session_state["history"]:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state["history"].append({"role": "user", "content": user_input})
    with st.chat_message("human"):
        st.text(user_input)

    response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]}, config=CONFIG)
    ai_message = response["messages"][-1].content
    st.session_state["history"].append({"role": "ai", "content": ai_message})
    with st.chat_message("ai"):
        st.text(ai_message)
    
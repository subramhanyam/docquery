import streamlit as st

st.set_page_config(page_title="Multi-Section App", layout="centered")

st.title("Welcome to the App")
st.write("Choose a section to explore:")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Basic Chatbot"):
        st.switch_page("pages\BasicChatbot.py")

with col2:
    if st.button("Multiple Files"):
        st.switch_page("pages\MultipleFiles.py")

with col3:
    if st.button("Web Query"):
        st.switch_page("pages\WebQuery.py")

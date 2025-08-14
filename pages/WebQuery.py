import streamlit as st
import uuid
from nodes import Graph, State
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Streamlit page setup
st.set_page_config(page_title="Web Loader", layout="centered")
st.title("🌐 Web Page Loader")
st.write("Enter a web URL to extract and embed its content.")

# Initialize session state
if "database" not in st.session_state:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    st.session_state["database"] = Chroma.from_documents([Document(page_content="")], embeddings)

if "combo" not in st.session_state:
    st.session_state["url_combo"] = {}

if "processed_urls" not in st.session_state:
    st.session_state["processed_urls"] = []

if  "id" not in st.session_state:
     st.session_state["id"] = str(uuid.uuid4())

# Input form
with st.form("web_loader_form"):
    url = st.text_input("Enter URL ", placeholder="https://example.com")
    submit = st.form_submit_button("Submit")

# Handle form submission
if submit and url:
    if url not in st.session_state["processed_urls"]:
        # Process via your graph loader
        graph = Graph()
        state = graph.graph.invoke(State(file=url))
        st.write("over")
        # Store metadata
        # st.session_state["id"] = str(uuid.uuid4())
        st.session_state["url_combo"].update({ st.session_state["id"]: url})
        st.session_state["processed_urls"].append(url)

        # for document in state["chunks"]:
        #     document.metadata.update({"file_id":  st.session_state["id"]})
        st.session_state["database"].add_documents(state["chunks"])

        st.success("✅ Web content successfully processed and embedded.")
        st.switch_page("pages/index2.py")  # redirect to index2 after processing
    else:
        st.info("This URL has already been processed.")

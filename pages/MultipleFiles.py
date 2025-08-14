import streamlit as st
import os
from configparser import ConfigParser
from nodes import Graph,State
from langchain_core.messages import HumanMessage
import uuid
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
# Ensure the 'files' directory exists
os.makedirs("files", exist_ok=True)

st.set_page_config(page_title="Stylish File Uploader", layout="centered")

# --- Custom CSS for styling the upload widget ---
st.markdown("""
    <style>
        .stFileUploader > label {
            background-color: #4CAF50;
            color: white;
            padding: 0.75em 1.5em;
            border-radius: 10px;
            font-weight: bold;
            cursor: pointer;
        }
        .stFileUploader > div > input {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title and description ---
st.title("📁 File Uploader")
st.write("Upload multiple files. They will be saved to the `files/` directory.")

# --- File uploader ---
uploaded_files = st.file_uploader(
    "Upload Files",
    type=None,         # Accept all file types
    accept_multiple_files=True,
    key="file_uploader"
)
if "files" not in st.session_state:
    st.session_state["files"]=[]
if "processed_file" not in st.session_state:
    st.session_state["processed_file"]=[]
if "database" not in st.session_state:
    embeddings=OpenAIEmbeddings(model="text-embedding-3-large")
    st.session_state["database"] =  Chroma.from_documents([Document(page_content="")],embeddings)

if "combo" not in st.session_state:
    st.session_state["combo"]={}
# --- Save uploaded files ---
if uploaded_files:
    
    for file in uploaded_files:
        if file.name not in st.session_state["files"]:
            file_path = os.path.join("files", file.name)
            st.session_state["files"].append(file.name)
            # config['UploadedFiles'][file.name] = file_path
            byte_data = file.read()
            with open(file_path, "wb") as f:
                f.write(byte_data)
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded and saved to `files/` folder.")
    # st.write(st.session_state["files"])
    #-----
    # embeddings=OpenAIEmbeddings(model="text-embedding-3-large")
    # vectordb = FAISS.from_documents([Document(page)],embeddings)
    info_msg = st.info("Converting...")
    if "n" not in st.session_state:
        st.session_state["n"] = 0
    n = st.session_state["n"]
    for file_name in st.session_state["files"]:
        if file_name not in st.session_state["processed_file"]:
            graph = Graph()
            state = graph.graph.invoke(State(file = file_name))
            st.session_state["processed_file"].append(file_name)
            st.session_state["id"] = str(uuid.uuid4())
            st.write(st.session_state["n"])
            st.session_state["combo"].update({st.session_state["id"]:st.session_state["files"][st.session_state["n"]]})
            st.session_state["n"] = st.session_state["n"]+1
            for documents in state["chunks"]:
                documents.metadata.update({"file_id": st.session_state["id"]})
                st.session_state["database"].add_documents([documents],metadata=documents.metadata)


        info_msg.empty()
        st.success(f"Done! converted{file.name} to embeddings")
# st.write(st.session_state["combo"])

# query = "Summarize the content of selected documents"
# file_ids = list(st.session_state["combo"].keys())
# if len(file_ids) != 0:

#     results = st.session_state["database"].similarity_search(
#         query=query,
#         k=5,
#         filter={"file_id": {"$in": file_ids}}
#     )
#     # st.write(results)
# class Casscade:
#     def __init__(self):
#         self.files = st.session_state["combo"]
#         self.database = st.session_state["database"]
# --- Submit button to go to index2.py ---
st.markdown("---")  # horizontal line for visual separation
st.write("When you're ready, click below to continue to the next step.")

if st.button("Go to Index2"):
    st.switch_page("pages/index2.py")


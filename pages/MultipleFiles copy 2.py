import streamlit as st
import os
from configparser import ConfigParser
from nodes import Graph
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
config = ConfigParser()
if 'UploadedFiles' not in config:
    config['UploadedFiles'] = {}
# --- Save uploaded files ---
if uploaded_files:
    
    for file in uploaded_files:
        file_path = os.path.join("files", file.name)
        st.session_state["files"].append(file.name)
        config['UploadedFiles'][file.name] = file_path
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded and saved to `files/` folder.")


with open(r"C:\Users\Administrator\Desktop\1602_24_733_186\doc_query\uiconfig_file.ini", "w") as configfile:
    config.write(configfile)


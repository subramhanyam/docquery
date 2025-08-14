import streamlit as st
import os
from configparser import ConfigParser
# Ensure the 'files' directory exists
from langchain_core import messages
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool
from langchain_community.vectorstores import Chroma
import uuid
#for pdf
@tool
def pdf_loader(pdf:str):
    """
    Loads and extracts text content from a PDF file using PyPDFLoader.

    Parameters:
        pdf (str): The path to the PDF file to be loaded.

    Returns:
        list: A list of documents (typically as LangChain Document objects) extracted from the PDF.
    """
    from langchain_community.document_loaders import PyPDFLoader
    loader=PyPDFLoader(pdf)
    docs=loader.load()
    return docs

#for text
@tool
def textloader(text:str):
    """
    Loads and extracts text content from a plain text file using TextLoader.

    Parameters:
        text (str): The path to the text file to be loaded.

    Returns:
        list: A list of documents (typically as LangChain Document objects) extracted from the text file.
    """
    from langchain_community.document_loaders import TextLoader
    loader=TextLoader(text)
    docs=loader.load()
    return docs

# text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
# documents=text_splitter.split_documents(docs)

#for web query

# from langchain_text_splitters import RecursiveCharacterTextSplitter

# text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
# documents=text_splitter.split_documents(docs)

from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
print(os.environ["OPENAI_API_KEY"])
llm=ChatOpenAI(model="gpt-4o")

tools=[pdf_loader,textloader]
llm_with_tools = llm.bind_tools(tools)
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
class State(TypedDict):
    messages:list[AnyMessage]
    


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

if 'databases' not in st.session_state:
    st.session_state["datbases"]={}
if "id" not in st.session_state:
    st.session_state["datbases"]=None

from configparser import ConfigParser
import streamlit as st
import os

class Config:
    def __init__(self,config_path = r"C:\Users\Administrator\Desktop\1602_24_733_186\doc_query\uiconfig.ini"):
        self.configparser = ConfigParser()
        self.configparser.read(config_path)
    
    def llm_options(self):
        return self.configparser["DEFAULT"].get("llm_Option").split(", ")
    
    # def usecase_options(self):
    #     return self.configparser["DEFAULT"].get("usecase_options").split(", ")
    
    def llm1_model_options(self):
        return self.configparser["DEFAULT"].get("llm1_model_options").split(", ")
    
    def llm2_model_options(self):
        return self.configparser["DEFAULT"].get("llm2_model_options").split(", ")
    
    # def page_title(self):
    #     return self.configparser["DEFAULT"].get("page_title")
    
class Loadui:
    def __init__(self):
        self.config = Config()
        self.user_choices = {}
    def load_streamlit_ui(self):
        # st.set_page_config(page_title=self.config.page_title())
        # st.header(self.config.page_title())

        with st.sidebar:
            llm_options = self.config.llm_options()
            # usecases = self.config.usecase_options()

            self.user_choices["select_llm"]=st.selectbox("select_llm",llm_options)
            
            
            if self.user_choices["select_llm"] == "OpenAI":
                model_options = self.config.llm1_model_options()
            else:
                model_options = self.config.llm2_model_options()
            
            self.user_choices["select_model_options"]=st.selectbox("select_model_options",model_options)
            self.user_choices["API_KEY"]=st.text_input("enter api key",type="password")

            if not self.user_choices["API_KEY"]:
                st.warning("please enter a api key")
            
            # self.user_choices["select_usecase"]=st.selectbox("select_usecase",usecases)
            if 'shared_data' in st.session_state:
                self.user_choices["select_files"]=st.selectbox("select_files",st.session_state.shared_data)


        if uploaded_files:
    
            for file in uploaded_files:
                file_path = os.path.join("files", file.name)
                st.session_state["files"].append(file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                info_msg = st.info("Converting...")
                from langchain_core.messages import HumanMessage
                from langchain.prompts import ChatPromptTemplate
                prompt = ChatPromptTemplate.from_messages([
                    ("system","you are a helper model"),
                    ("user","process this file {file}")
                ])
                # prompt.invoke({"file":"sample.txt"}).messages
                chain = prompt | llm_with_tools
                result = chain.invoke({"file":f"files\{file.name}"})
                tool_mapping={"pdf_loader":pdf_loader,"textloader":textloader}
                for tool_call in result.tool_calls:
                    tool = tool_mapping[tool_call["name"]]
                    tool_output = tool.invoke(tool_call)     
                    # messages.append(messages.ToolMessage(tool_output,tool_call_id=tool_call["id"]))
                text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
                documents=text_splitter.split_documents(tool_output.content)
                # info_msg = st.info("Converting...")
                embeddings=OpenAIEmbeddings(model="text-embedding-3-large",api_key=self.user_choices["API_KEY"])
                st.session_state["id"] = str(uuid.uuid4())
                st.session_state["datbases"].update({st.session_state["id"]:Chroma.from_documents(documents,embeddings)})
                info_msg.empty()
                config['UploadedFiles'][file.name] = st.session_state["id"]
                st.success(f"Done! converted{file.name} to embeddings")
                



            st.success(f"✅ {len(uploaded_files)} file(s) uploaded and saved to `files/` folder.")
            self.databases = st.session_state["databases"]

        with open(r"C:\Users\Administrator\Desktop\1602_24_733_186\doc_query\uiconfig_file.ini", "w") as configfile:
            config.write(configfile)
        return self.user_choices
    
def load_agentic_ai_app():

    ui = Loadui()
    user_input = ui.load_streamlit_ui()


if __name__ == "__main__":
    load_agentic_ai_app()



# --- Save uploaded files ---
# if uploaded_files:
    
#     for file in uploaded_files:
#         file_path = os.path.join("files", file.name)
#         st.session_state["files"].append(file.name)
#         with open(file_path, "wb") as f:
#             f.write(file.getbuffer())
#         from langchain_core.messages import HumanMessage
#         from langchain.prompts import ChatPromptTemplate
#         prompt = ChatPromptTemplate.from_messages([
#             ("system","you are a helper model"),
#             ("user","process this file {file}")
#         ])
#         prompt.invoke({"file":"sample.txt"}).messages
#         chain = prompt | llm_with_tools
#         result = chain.invoke({"file":"sample.txt"})
#         tool_mapping={"pdf_loader":pdf_loader,"textloader":textloader}
#         for tool_call in result.tool_calls:
#             tool = [tool_call["name"]]
#             tool_output = tool.invoke(tool_call)     
#             # messages.append(messages.ToolMessage(tool_output,tool_call_id=tool_call["id"]))
#         text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
#         documents=text_splitter.split_documents(tool_output.content)
#         info_msg = st.info("Converting...")
#         embeddings=OpenAIEmbeddings(model="text-embedding-3-large")
#         st.session_state["id"] = str(uuid.uuid4())
#         st.session_state["datbases"].update({st.session_state["id"]:Chroma.from_documents(documents,embeddings)})
#         info_msg.empty()
#         config['UploadedFiles'][file.name] = st.session_state["id"]
#         st.success(f"Done! converted{file.name} to embeddings")




#     st.success(f"✅ {len(uploaded_files)} file(s) uploaded and saved to `files/` folder.")


# with open(r"C:\Users\Administrator\Desktop\1602_24_733_186\doc_query\uiconfig_file.ini", "w") as configfile:
#     config.write(configfile)
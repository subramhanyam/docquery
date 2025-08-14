from typing_extensions import TypedDict,Annotated
from langchain_core.messages import AnyMessage,HumanMessage
from langgraph.graph import add_messages
from langchain_core.documents import Document
from langchain_core.tools import tool
class State(TypedDict):
    # messages: Annotated[list[AnyMessage],add_messages]

    file : str
    documents: list[Document]
    chunks : list[Document]

from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
print(os.environ["OPENAI_API_KEY"])
llm=ChatOpenAI(model="gpt-4o")
def webbase_loader(state: State):
    """
    Loads and extracts text content from a web page using WebBaseLoader.

    Parameters:
        state (State): The state object containing the URL to be loaded.

    Returns:
        dict: A dictionary containing a list of documents extracted from the web page.
    """
    from langchain_community.document_loaders import WebBaseLoader

    loader = WebBaseLoader(state["file"])
    docs = loader.load()
    # message = state["messages"][-1]
    # result = llm_with_tools.invoke(message.tool_calls)
    
    return {"documents": docs}


def pdf_loader(state : State):
    """
    Loads and extracts text content from a PDF file using PyPDFLoader.

    Parameters:
        pdf (str): The path to the PDF file to be loaded.

    Returns:
        list: A list of documents (typically as LangChain Document objects) extracted from the PDF.
    """
    from langchain_community.document_loaders import PyPDFLoader
    loader=PyPDFLoader(state["file"])
    docs=loader.load()
    # message = state["messages"][-1]
    # reuslt= llm_with_tools.invoke(message.tool_calls)
    return {"documents":docs}

def textloader(state : State):
    """
    Loads and extracts text content from a plain text file using TextLoader.

    Parameters:
        text (str): The path to the text file to be loaded.

    Returns:
        list: A list of documents (typically as LangChain Document objects) extracted from the text file.
    """
    from langchain_community.document_loaders import TextLoader
    loader=TextLoader("files/" + state["file"],autodetect_encoding= True)
    docs=loader.load()
    return State(documents=docs)
tools=[pdf_loader,textloader]
llm_with_tools = llm.bind_tools(tools)
from pydantic import BaseModel,Field
from typing import Literal
class Types(BaseModel):
    type : Literal["pdf","txt","webbase_loader"]=Field(description="You are a helpful assistant that determines the type of input based on the provided file name, file path, or URL. Use the file extension or input pattern to choose the appropriate loading method. If the input ends with .pdf, route the request to the pdf_loader. If the input ends with .txt, route the request to the text_loader. If the input is a URL starting with http:// or https://, or if it ends with .xml, route the request to the webbase_loader to extract content from the web page or XML sitemap. Ensure the correct loader is used based on the input type to accurately extract the content.")
def router(state:State):
    llm_struct = llm.with_structured_output(Types)
    result = llm_struct.invoke(state["file"])
    if result.type == 'pdf':
        return "pdf_loader"
    elif result.type == "webbase_loader":
        return "webbase_loader"
    return "textloader"
def llm_call(state:State):
    # llm_with_tools = llm.bind_tools(tools)
    # result = llm_with_tools.invoke(state["messages"])
    # if len(result.tool_calls) != 0: 
    #     file_name = result.tool_calls[0]["args"]["state"]["file"]
    return {"file":state["file"]}
    # return State(messages=[result])
from langchain_text_splitters import RecursiveCharacterTextSplitter
def chunks(state:State):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=100)
    documents=text_splitter.split_documents(state["documents"])
    return {"chunks":documents}
from langgraph.graph import START,END,StateGraph
# from langgraph.prebuilt import ToolNode,tools_condition

graph_builder = StateGraph(State)
graph_builder.add_node('llm_call',llm_call)
graph_builder.add_node("webbase_loader",webbase_loader)
graph_builder.add_node("pdf_loader",pdf_loader)
graph_builder.add_node("textloader",textloader)
graph_builder.add_node("chunks",chunks)

graph_builder.add_edge(START,"llm_call")
graph_builder.add_conditional_edges("llm_call",router,{"pdf_loader":"pdf_loader","textloader":"textloader","webbase_loader":"webbase_loader"})
graph_builder.add_edge("pdf_loader","chunks")
graph_builder.add_edge("textloader","chunks")
graph_builder.add_edge("webbase_loader","chunks")
graph_builder.add_edge("chunks",END)
graph = graph_builder.compile()

class Graph:
    graph = graph
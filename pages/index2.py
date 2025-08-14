import streamlit as st
from configparser import ConfigParser
import streamlit as st
import os
from langchain import hub
# from pages.MultipleFiles import Casscade
# casscade = Casscade()

if "ids" not in st.session_state:
    st.session_state["ids"] = []
if "database" not in st.session_state:
    st.session_state["database"] = None

from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
print(os.environ["OPENAI_API_KEY"])
llm=ChatOpenAI(model="gpt-4o")
class Config:
    def __init__(self,config_path = r"C:\Users\Administrator\Desktop\1602_24_733_186\AGENTICWORKSPACE\AGENTICCHATBOT\src\langgraphagenticai\Ui\uiconfig.ini"):
        self.configparser = ConfigParser()
        self.configparser.read(config_path)
    
    def llm_options(self):
        return self.configparser["DEFAULT"].get("llm_Option").split(", ")
    
    def usecase_options(self):
        return self.configparser["DEFAULT"].get("usecase_options").split(", ")
    
    def llm1_model_options(self):
        return self.configparser["DEFAULT"].get("llm1_model_options").split(", ")
    
    def llm2_model_options(self):
        return self.configparser["DEFAULT"].get("llm2_model_options").split(", ")
    
    def page_title(self):
        return self.configparser["DEFAULT"].get("page_title")
    
class Loadui:
    def __init__(self):
        self.config = Config()
        self.user_choices = {}
    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.page_title())
        st.header(self.config.page_title())
        # st.write("starting")
        # st.write(st.session_state["combo"])
        # st.write("ending")
        with st.sidebar:
            st.markdown("### 🔀 Navigate")
    
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Index1"):
                    st.switch_page("index1.py")
            with col2:
                if st.button("Docs"):
                    st.switch_page("pages/MultipleFiles.py")
            with col3:
                if st.button("Web"):
                    st.switch_page("pages/WebQuery.py")

            st.markdown("---")
            llm_options = self.config.llm_options()
            usecases = self.config.usecase_options()

            self.user_choices["select_llm"]=st.selectbox("select_llm",llm_options)
            
            
            if self.user_choices["select_llm"] == "llm1":
                model_options = self.config.llm1_model_options()
            else:
                model_options = self.config.llm2_model_options()
            
            self.user_choices["select_model_options"]=st.selectbox("select_model_options",model_options)
            self.user_choices["API_KEY"]=st.text_input("enter api key",type="password")

            if not self.user_choices["API_KEY"]:
                st.warning("please enter a api key")
            
            # self.user_choices["select_usecase"]=st.selectbox("select_usecase",usecases,index = 0)
            # if 'shared_data' in st.session_state:
            #     self.user_choices["select_files"]=st.selectbox("select_files",st.session_state.shared_data)
            if "combo" in st.session_state:
                hobby = st.multiselect("select files",st.session_state["combo"].values())
                st.session_state["ids"] = []
                for file in hobby:
                    for id in st.session_state["combo"].keys():
                        if file == st.session_state["combo"][id]:
                            st.session_state["ids"].append(id) 
            elif "url_combo" in st.session_state:
                st.write(f"url is {str(st.session_state["url_combo"].values())}")
                st.session_state["ids"] = []
                # st.session_state["ids"].append("".join(list(st.session_state["url_combo"].keys()))) 
        return self.user_choices


def load_agentic_ai_app():

    ui = Loadui()
    user_input = ui.load_streamlit_ui()

    user_message = st.chat_input("enter something")
    # st.session_state['database'] = casscade.database
    prompt = hub.pull("rlm/rag-prompt")
    chain = prompt | llm
    if user_message:
        if len(st.session_state["ids"]) != 0:
            results = st.session_state["database"].similarity_search(
                query=user_message,
                k=5,
                filter={"file_id": {"$in": st.session_state["ids"]}}
            )


        
    
            result = chain.invoke({"context": f"{results}", "question": f"{user_message}"})
            with st.chat_message("user"):
                st.write(user_message)

            with st.chat_message("ai"):
                st.write(result.content)
        else:
            if (st.session_state["database"]):

                results = st.session_state["database"].similarity_search(
                query=user_message,
                )


        
    
                result = chain.invoke({"context": f"{results}", "question": f"{user_message}"})
                with st.chat_message("user"):
                    st.write(user_message)

                with st.chat_message("ai"):
                    st.write(result.content)
            else:
                result = chain.invoke({"context": f"no context answer only based on user question", "question": f"{user_message}"})
                with st.chat_message("user"):
                    st.write(user_message)

                with st.chat_message("ai"):
                    st.write(result.content)


if __name__ == "__main__":
    load_agentic_ai_app()
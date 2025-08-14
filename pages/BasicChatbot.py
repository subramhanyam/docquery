from configparser import ConfigParser
import streamlit as st
import os

# class Config:
#     def __init__(self,config_path = r"C:\Users\Administrator\Desktop\1602_24_733_186\AGENTICWORKSPACE\AGENTICCHATBOT\src\langgraphagenticai\Ui\uiconfig.ini"):
#         self.configparser = ConfigParser()
#         self.configparser.read(config_path)
    
#     def llm_options(self):
#         return self.configparser["DEFAULT"].get("llm_Option").split(", ")
    
#     def usecase_options(self):
#         return self.configparser["DEFAULT"].get("usecase_options").split(", ")
    
#     def llm1_model_options(self):
#         return self.configparser["DEFAULT"].get("llm1_model_options").split(", ")
    
#     def llm2_model_options(self):
#         return self.configparser["DEFAULT"].get("llm2_model_options").split(", ")
    
#     def page_title(self):
#         return self.configparser["DEFAULT"].get("page_title")
    
# class Loadui:
#     def __init__(self):
#         self.config = Config()
#         self.user_choices = {}
#     def load_streamlit_ui(self):
#         st.set_page_config(page_title=self.config.page_title())
#         st.header(self.config.page_title())

#         with st.sidebar:
#             llm_options = self.config.llm_options()
#             usecases = self.config.usecase_options()

#             self.user_choices["select_llm"]=st.selectbox("select_llm",llm_options)
            
            
#             if self.user_choices["select_llm"] == "llm1":
#                 model_options = self.config.llm1_model_options()
#             else:
#                 model_options = self.config.llm2_model_options()
            
#             self.user_choices["select_model_options"]=st.selectbox("select_model_options",model_options)
#             self.user_choices["API_KEY"]=st.text_input("enter api key",type="password")

#             if not self.user_choices["API_KEY"]:
#                 st.warning("please enter a api key")
            
#             self.user_choices["select_usecase"]=st.selectbox("select_usecase",usecases)
#             if 'shared_data' in st.session_state:
#                 self.user_choices["select_files"]=st.selectbox("select_files",st.session_state.shared_data)

#         return self.user_choices
    
# def load_agentic_ai_app():

#     ui = Loadui()
#     user_input = ui.load_streamlit_ui()

#     user_message = st.chat_input("enter something")
#     if user_message:
#         st.write(user_message)

# if __name__ == "__main__":
#     load_agentic_ai_app()
st.switch_page("pages/index2.py")
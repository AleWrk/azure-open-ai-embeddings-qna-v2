import streamlit as st
import os
import traceback
from utilities.helper import LLMHelper
from pathlib import Path

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

@st.cache_resource()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    # Set page layout to wide screen and menu item
    menu_items = {
	'Get help': None,
	'Report a bug': None,
	'About': '''
	 ## Embeddings App

	Document Reader Sample Demo.
	'''
    }
    st.set_page_config(layout="wide", page_title="Innovation & Processes - GenAI PoC", page_icon=":robot_face:")

    st.markdown(read_markdown_file("markdown/styles.md").replace('{img-isp}', get_base64_of_bin_file(os.path.join('images', 'isp-logo.png'))).replace('{img-isl}', get_base64_of_bin_file(os.path.join('images', 'isl-logo.png'))).replace('{title}',os.environ['POC_TITLE']), unsafe_allow_html=True)

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    llm_helper = LLMHelper()

    col1, col2, col3 = st.columns([2,1,1])

    files_data = llm_helper.blob_client.get_all_files()

    st.dataframe(files_data, use_container_width=True)

except Exception as e:
    st.error(traceback.format_exc())

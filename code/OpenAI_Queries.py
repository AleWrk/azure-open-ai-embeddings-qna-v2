import base64
import logging
import os
import traceback
import logging
import re
from pathlib import Path
from annotated_text import annotated_text

import streamlit as st
from dotenv import load_dotenv
from st_pages import add_page_title, show_pages_from_config
from utilities.helper import LLMHelper

load_dotenv()


logger = logging.getLogger(
    'azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)


def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

@st.cache_resource()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    default_question = ""
    default_answer = ""

    if 'question' not in st.session_state:
        st.session_state['question'] = default_question
    if 'response' not in st.session_state:
        st.session_state['response'] = default_answer
    if 'context' not in st.session_state:
        st.session_state['context'] = ""
    if 'custom_prompt' not in st.session_state:
        st.session_state['custom_prompt'] = ""
    if 'custom_temperature' not in st.session_state:
        st.session_state['custom_temperature'] = float(
            os.getenv("OPENAI_TEMPERATURE", 0.7))
        

    # Set page layout to wide screen and menu item
    menu_items = {
        'Get help': None,
        'Report a bug': None,
        'About': '''	        
	    Demo Generative AI Made with :heart: by Innovation Team
	    '''
    }
    st.set_page_config(layout="wide", menu_items=menu_items, page_title="Innovation & Processes - GenAI PoC", page_icon=":robot_face:")

    llm_helper = LLMHelper(custom_prompt=st.session_state.custom_prompt,
                           temperature=st.session_state.custom_temperature)
    
    def applycnfg():
        st.session_state['is_exp'] = False
        llm_helper = LLMHelper(max_tokens=st.session_state['tklen'])


    if 'is_exp' not in st.session_state:
        st.session_state['is_exp'] = False


    col1, col2, col3 = st.columns([2, 2, 2])
    with col3:
        with st.expander("Settings", expanded=st.session_state['is_exp']):
            st.session_state['tklen'] =st.tokens_response = st.slider(
                "Tokens response length", 100, 1000, 500)
            aplychng = st.button("Apply", key="apply_chat", on_click=applycnfg)
    

    show_pages_from_config()
    st.markdown(read_markdown_file("markdown/styles.md").replace('{img-isp}', get_base64_of_bin_file(os.path.join('images', 'isp-logo.png'))).replace('{img-isl}', get_base64_of_bin_file(os.path.join('images', 'isl-logo.png'))).replace('{title}',os.environ['POC_TITLE']), unsafe_allow_html=True)

    st.title("Generative Search")
    st.header("In questa sezione è possibile effettuare una ricerca all'interno della knowledge base. La risposta sarà generata dal modello sulla base dei documenti elencati.\n\n")
    st.write("")

    def search_from_data(qst):        
        st.session_state['question']=qst
    
    st.session_state.run = False
    col1, col2 = st.columns([5, 1])
    with col1:
        question = st.text_input("Inserire il testo da ricercare e premere Cerca", )    
    with col2:
        st.button("Cerca", key="search_chat", on_click=search_from_data(question), disabled=st.session_state.run)
    
    result_area = st.empty()
    
    if st.session_state['question']!="" and st.session_state['question']!=default_question :
        with st.spinner('**Generazione risposta...**'):
            default_question = st.session_state['question']
            result_area.empty()        
            st.session_state['question'] = question
            st.session_state['question'], st.session_state['response'], st.session_state[
                'context'], sources = llm_helper.get_semantic_answer_lang_chain(question, [])
            response = st.session_state['response']
            responses = re.split('fonti utilizzate:', response, flags=re.IGNORECASE)
            st.markdown(responses[0])
            if len(responses) > 1:
                st.markdown("**Riferimenti:**")
                st.markdown(responses[1].replace('.txt', ''))
            st.divider()
            st.markdown(f'\n\n**Testi consultati dal modello:**\n')
            st.session_state['question']=""
            for index, source in enumerate(sorted(sources.split())):
                annotated_text((source, 'PDF', "#b3d6fb"))
            st.divider()

            with st.expander("Testo passato nel contesto"):
                st.markdown(st.session_state['context'].replace('$', '\$'))            
                st.markdown(f"FONTI: {sources}")        

except Exception:
    st.error(traceback.format_exc())

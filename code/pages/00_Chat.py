import streamlit as st
from streamlit_chat import message
import os
from utilities.helper import LLMHelper


llm_helper = LLMHelper()

if 'is_exp' not in st.session_state:
    st.session_state['is_exp'] = False



def applycnfg():
    st.session_state['is_exp'] = False
     
    print(st.session_state['is_exp'])
    llm_helper = LLMHelper(max_tokens=st.session_state['tklen'])


col1, col2, col3 = st.columns([2, 2, 2])
with col3:
    with st.expander("Settings", expanded=st.session_state['is_exp']):
        st.session_state['tklen'] =st.tokens_response = st.slider(
            "Tokens response length", 100, 1000, 500)
        aplychng = st.button("Apply", key="apply_chat", on_click=applycnfg)


def clear_text_input():
    st.session_state['question'] = st.session_state['input']
    st.session_state['input'] = ""

def clear_chat_data():
    st.session_state['input'] = ""
    st.session_state['chat_history'] = []
    st.session_state['source_documents'] = []


        


# Initialize chat history
if 'question' not in st.session_state:
    st.session_state['question'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'source_documents' not in st.session_state:
    st.session_state['source_documents'] = []



def search_from_data():
    st.session_state['question'] = valueent
    st.session_state['input'] = ""
    
    if st.session_state['question']:
        question, result, _, sources = llm_helper.get_semantic_answer_lang_chain(st.session_state['question'], st.session_state['chat_history'])
        st.session_state['chat_history'].append((question, result))
        st.session_state['source_documents'].append(sources)
        st.session_state['question']=""
    if st.session_state['chat_history']:
        #for i in range(len(st.session_state['chat_history'])-1, -1, -1):
        #print(st.session_state['chat_history'])
        for i in range(len(st.session_state['chat_history'])):
            print(st.session_state['chat_history'][i])
            message(st.session_state['chat_history'][i][0], is_user=True, key=str(i) + '_user')
            message(st.session_state['chat_history'][i][1], key=str(i))
            #st.markdown(f'\n\nSources: {st.session_state["source_documents"][i]}')


# Chat 
#st.text_input("You: ", placeholder="type your question", key="input", on_change=clear_text_input)
valueent = st.text_input("You: ", placeholder="type your question", key="input")
btnsearch = st.button("Search", key="search_chat", on_click=search_from_data)
clear_chat = st.button("Clear chat", key="clear_chat", on_click=clear_chat_data)

js = f"""
<script>
    function scroll(dummy_var_to_force_repeat_execution){{
        var textAreas = parent.document.querySelectorAll('section.main');
        for (let index = 0; index < textAreas.length; index++) {{
            textAreas[index].scrollTop = textAreas[index].scrollHeight;
        }}
    }}
    scroll({len(st.session_state['chat_history'])})
</script>
"""
st.components.v1.html(js)

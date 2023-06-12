import streamlit as st
from streamlit_chat import message
from utilities.helper import LLMHelper

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
        for i in range(len(st.session_state['chat_history'])-1, -1, -1):
            message(st.session_state['chat_history'][i][0], is_user=True, key=str(i) + '_user')
            message(st.session_state['chat_history'][i][1], key=str(i))
            st.markdown(f'\n\nSources: {st.session_state["source_documents"][i]}')
            
    

    


llm_helper = LLMHelper()

# Chat 
#st.text_input("You: ", placeholder="type your question", key="input", on_change=clear_text_input)
valueent = st.text_input("You: ", placeholder="type your question", key="input")
btnsearch = st.button("Search", key="search_chat", on_click=search_from_data)
clear_chat = st.button("Clear chat", key="clear_chat", on_click=clear_chat_data)



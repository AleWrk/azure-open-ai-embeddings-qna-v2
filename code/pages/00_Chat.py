import streamlit as st
from streamlit_chat import message
import os
import re
from annotated_text import annotated_text
from pathlib import Path
from utilities.helper import LLMHelper


llm_helper = LLMHelper()

if 'is_exp' not in st.session_state:
    st.session_state['is_exp'] = False

def applycnfg():
    st.session_state['is_exp'] = False
     
    #print(st.session_state['is_exp'])
    llm_helper = LLMHelper(max_tokens=st.session_state['tklen'])

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

@st.cache_resource()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.set_page_config(layout="wide", page_title="Innovation - GenAI PoC", page_icon=":robot_face:")

col1, col2, col3 = st.columns([2, 2, 2])
with col3:
    with st.expander("Settings", expanded=st.session_state['is_exp']):
        st.session_state['tklen'] =st.tokens_response = st.slider(
            "Tokens response length", 100, 1000, 500)
        aplychng = st.button("Apply", key="apply_chat", on_click=applycnfg)


def clear_chat_data():
    st.session_state['question'] = ""
    st.session_state['chat_history'] = []
    st.session_state['source_documents'] = [""]
    st.session_state['past'] = ['Ciao!']
    st.session_state['generated'] = ["Ciao, sono il chatbot 'Generativo': come posso aiutarti?"]

# Initialize chat history
if 'question' not in st.session_state:
    st.session_state['question'] = ""
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'source_documents' not in st.session_state:
    st.session_state['source_documents'] = [""]
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Ciao, sono il chatbot 'Generativo': come posso aiutarti?"]
if 'past' not in st.session_state:
    st.session_state['past'] = ['Ciao!']

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
print(st.session_state['question'])

st.markdown(read_markdown_file("markdown/styles.md").replace('{img-isp}', get_base64_of_bin_file(os.path.join('images', 'isp-logo.png'))).replace('{img-isl}', get_base64_of_bin_file(os.path.join('images', 'isl-logo.png'))).replace('{title}',os.environ['POC_TITLE']), unsafe_allow_html=True)

st.title("Generative Chatbot")
st.header("In questa sezione è possibile dialogare con un chatbot realizzato dal modello generativo. Il chatbot risponderà basandosi esclusivamente sui documenti presenti nella knowledge base.\n\n")
st.write("")

def generate_response():
    if st.session_state['question']:
        print('Gli passo la domanda: ', st.session_state['question'])
        print('Con storico chat: ', st.session_state['chat_history'])
        question, result, _, sources = llm_helper.get_semantic_answer_lang_chain(st.session_state['question'], st.session_state['chat_history'])
        st.session_state['chat_history'].append((question, result))
        st.session_state['source_documents'].append(sources)        
        response = re.split('fonti utilizzate:', result, flags=re.IGNORECASE)
        result = response[0]
        refs = ""
        
        if len(response) > 1:
            refs = "Riferimenti:"
            refs += response[1].replace('.txt', '')
            result += refs

    return result
    
js = f"""
<script>
    function scroll(dummy_var_to_force_repeat_execution){{
        var textAreas = parent.document.querySelectorAll('section.main');
        for (let index = 0; index < textAreas.length; index++) {{
            textAreas[index].scrollTop = textAreas[index].scrollHeight;
        }}
    }}
    scroll({len(st.session_state['generated'])})
</script>
"""


response_container = st.container()
input_container = st.container()

## Applying the user input box
with input_container:
    col1, col2 = st.columns([5, 1])
    with col1:
        input = st.text_input("Digita il testo e premi invio. Utilizza il pulsante per pulire il contesto della chat.", key="question")
        
    with col2:
        st.button("Pulisci Chat", on_click=clear_chat_data)

with response_container:

    if st.session_state['question']!="":
        response = generate_response()
        print('sto appendendo la domanda: ', st.session_state['question'])
        st.session_state.past.append(st.session_state['question'])
        st.session_state.generated.append(response)
        
        
        
        
    if st.session_state['generated']:
        
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user', avatar_style="adventurer")
            message(st.session_state["generated"][i], key=str(i), avatar_style="shapes")
            if len(st.session_state['source_documents'][i])>0:
                st.markdown(f'\n\n**Testi consultati dal modello:**\n')            
                for index, source in enumerate(sorted(st.session_state['source_documents'][i].split())):
                    annotated_text((source, 'PDF', "#b3d6fb"))
    
    st.divider()
    if (len(st.session_state['generated']))>1:
        st.components.v1.html(js, height=0, width=0)
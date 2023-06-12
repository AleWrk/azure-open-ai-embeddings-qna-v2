import base64
import logging
import os
import traceback
import logging
from pathlib import Path
from annotated_text import annotated_text

import streamlit as st
from dotenv import load_dotenv
from st_pages import add_page_title, show_pages_from_config
from utilities.helper import LLMHelper

load_dotenv()


logger = logging.getLogger(
    'azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)


def check_deployment():
    # Check if the deployment is working
    # \ 1. Check if the llm is working
    try:
        llm_helper = LLMHelper()
        llm_helper.get_completion("Generate a joke!")
        st.success("LLM is working!")
    except Exception as e:
        st.error(f"""LLM is not working.  
            Please check you have a deployment name {llm_helper.deployment_name} in your Azure OpenAI resource {llm_helper.api_base}.  
            If you are using an Instructions based deployment (text-davinci-003), please check you have an environment variable OPENAI_DEPLOYMENT_TYPE=Text or delete the environment variable OPENAI_DEPLOYMENT_TYPE.  
            If you are using a Chat based deployment (gpt-35-turbo or gpt-4-32k or gpt-4), please check you have an environment variable OPENAI_DEPLOYMENT_TYPE=Chat.  
            Then restart your application.
            """)
        st.error(traceback.format_exc())
    # \ 2. Check if the embedding is working
    try:
        llm_helper = LLMHelper()
        llm_helper.embeddings.embed_documents(texts=["This is a test"])
        st.success("Embedding is working!")
    except Exception as e:
        st.error(f"""Embedding model is not working.  
            Please check you have a deployment named "text-embedding-ada-002" for "text-embedding-ada-002" model in your Azure OpenAI resource {llm_helper.api_base}.  
            Then restart your application.
            """)
        st.error(traceback.format_exc())
    # \ 3. Check if the translation is working
    try:
        llm_helper = LLMHelper()
        llm_helper.translator.translate("This is a test", "it")
        st.success("Translation is working!")
    except Exception as e:
        st.error(f"""Translation model is not working.  
            Please check your Azure Translator key in the App Settings.  
            Then restart your application.  
            """)
        st.error(traceback.format_exc())
    # \ 4. Check if the Redis is working with previous version of data
    try:
        llm_helper = LLMHelper()
        if llm_helper.vector_store.check_existing_index("embeddings-index"):
            st.warning("""Seems like you're using a Redis with an old data structure.  
            If you want to use the new data structure, you can start using the app and go to "Add Document" -> "Add documents in Batch" and click on "Convert all files and add embeddings" to reprocess your documents.  
            To remove this working, please delete the index "embeddings-index" from your Redis.  
            If you prefer to use the old data structure, please change your Web App container image to point to the docker image: fruocco/oai-embeddings:2023-03-27_25. 
            """)
        else:
            st.success("Redis is working!")
    except Exception as e:
        st.error(f"""Redis is not working. 
            Please check your Redis connection string in the App Settings.  
            Then restart your application.
            """)
        st.error(traceback.format_exc())


def check_variables_in_prompt():
    # Check if "summaries" is present in the string custom_prompt
    if "{summaries}" not in st.session_state.custom_prompt:
        st.warning("""Your custom prompt doesn't contain the variable "{summaries}".  
        This variable is used to add the content of the documents retrieved from the VectorStore to the prompt.  
        Please add it to your custom prompt to use the app.  
        Reverting to default prompt.
        """)
        st.session_state.custom_prompt = ""
    if "{question}" not in st.session_state.custom_prompt:
        st.warning("""Your custom prompt doesn't contain the variable "{question}".  
        This variable is used to add the user's question to the prompt.  
        Please add it to your custom prompt to use the app.  
        Reverting to default prompt.  
        """)
        st.session_state.custom_prompt = ""

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

@st.cache_resource()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache_data()
def get_languages():
    return llm_helper.translator.get_available_languages()


try:
    default_prompt = ""
    default_question = ""
    default_answer = ""

    if 'question' not in st.session_state:
        st.session_state['question'] = default_question
    # if 'prompt' not in st.session_state:
    #     st.session_state['prompt'] = os.getenv("QUESTION_PROMPT", "Please reply to the question using only the information present in the text above. If you can't find it, reply 'Not in the text'.\nQuestion: _QUESTION_\nAnswer:").replace(r'\n', '\n')
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
	 ## Embeddings App
	 Embedding testing application.
	'''
    }
    st.set_page_config(layout="wide", menu_items=menu_items)

    llm_helper = LLMHelper(custom_prompt=st.session_state.custom_prompt,
                           temperature=st.session_state.custom_temperature)
    
    # Get available languages for translation
    available_languages = get_languages()

    # Custom prompt variables
    custom_prompt_placeholder = """{summaries}  
    Rispondi in maniera discorsiva e completa alla domanda usando solo le informazioni presenti nel testo sopra. Se non riesci a trovarla, rispondi "Non presente nel testo".  
    Question: {question}  
    Answer:"""
    custom_prompt_help = """You can configure a custom prompt by adding the variables {summaries} and {question} to the prompt.  
    {summaries} will be replaced with the content of the documents retrieved from the VectorStore.  
    {question} will be replaced with the user's question.
        """    
    col1, col2, col3 = st.columns([2, 2, 2])
    with col3:
        with st.expander("Settings"):
            st.button("Check deployment", on_click=check_deployment)
            model = st.selectbox("OpenAI GPT-3 Model",
                                 [os.environ['OPENAI_ENGINE']])
            st.tokens_response = st.slider(
                "Tokens response length", 100, 1000, 500)
            st.slider("Temperature", min_value=0.0, max_value=1.0,
                      step=0.1, key='custom_temperature')
            #st.text_area("Custom Prompt", key='custom_prompt', on_change=check_variables_in_prompt,
            #             placeholder=custom_prompt_placeholder, help=custom_prompt_help, height=150)
            st.selectbox("Language", [
                         None] + list(available_languages.keys()), key='translation_language')
    
    show_pages_from_config()
    st.markdown(read_markdown_file("markdown/styles.md").replace('{img-isp}', get_base64_of_bin_file(os.path.join('images', 'isp-logo.png'))).replace('{img-isl}', get_base64_of_bin_file(os.path.join('images', 'isl-logo.png'))).replace('{title}',os.environ['POC_TITLE']), unsafe_allow_html=True)

    st.title("Generative Search")
    st.header("In questa sezione è possibile effettuare una ricerca all'interno della knowledge base. La risposta sarà generata dal modello sulla base dei documenti elencati.\n\n")
    st.write("")

    question = st.text_input("Inserire il testo da ricercare e premere invio", default_question)    

    
    if question != '':
        st.session_state['question'] = question
        st.session_state['question'], st.session_state['response'], st.session_state[
            'context'], sources = llm_helper.get_semantic_answer_lang_chain(question, [])
        response = st.session_state['response']
        st.markdown(response)        
        st.divider()
        st.markdown(f'\n\n**Testi consultati dal modello:**\n')
        for index, source in enumerate(sources.split()):
            annotated_text((source, str(index+1), "#b3d6fb"))
        st.divider()
        with st.expander("Testo passato nel contesto"):
            st.markdown(st.session_state['context'].replace('$', '\$'))            
            st.markdown(f"FONTI: {sources}")

    if st.session_state['translation_language'] and st.session_state['translation_language'] != '':
        st.write(f"Translation to other languages, 翻译成其他语言, النص باللغة العربية")
        st.write(
            f"{llm_helper.translator.translate(st.session_state['response'], available_languages[st.session_state['translation_language']])}")

except Exception:
    st.error(traceback.format_exc())

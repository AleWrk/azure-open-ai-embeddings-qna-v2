import streamlit as st
import os
import traceback
from utilities.helper import LLMHelper
from pathlib import Path

def delete_embedding():
    llm_helper.vector_store.delete_keys([f"doc:{st.session_state['embedding_to_drop']}"])

def delete_file():
    embeddings_to_delete = data[data.filename == st.session_state['file_to_drop']].key.tolist()
    embeddings_to_delete = list(map(lambda x: f"doc:{x}", embeddings_to_delete))
    llm_helper.vector_store.delete_keys(embeddings_to_delete)

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
	 Embedding testing application.
	'''
    }
    st.set_page_config(layout="wide", page_title="Innovation - GenAI PoC", page_icon=":robot_face:")

    st.markdown(read_markdown_file("markdown/styles-nobutton.md").replace('{img-isp}', get_base64_of_bin_file(os.path.join('images', 'isp-logo.png'))).replace('{img-isl}', get_base64_of_bin_file(os.path.join('images', 'isl-logo.png'))).replace('{title}',os.environ['POC_TITLE']), unsafe_allow_html=True)

    llm_helper = LLMHelper()

    # Query RediSearch to get all the embeddings
    data = llm_helper.get_all_documents(k=1000)

    if len(data) == 0:
        st.warning("No embeddings found. Go to the 'Add Document' tab to insert your docs.")
    else:
        st.dataframe(data, use_container_width=True)

        st.download_button("Download data", data.to_csv(index=False).encode('utf-8'), "embeddings.csv", "text/csv", key='download-embeddings')

        st.text("")
        st.text("")
        col1, col2, col3, col4 = st.columns([3,2,2,1])
        with col1:
            st.selectbox("Embedding id to delete", data.get('key',[]), key="embedding_to_drop")
        with col2:
            st.text("")
            st.text("")
            st.button("Delete embedding", on_click=delete_embedding)
        with col3:
            st.selectbox("File name to delete", set(data.get('filename',[])), key="file_to_drop")
        with col4:
            st.text("")
            st.text("")
            st.button("Delete file", on_click=delete_file)

        st.text("")
        st.text("")
        st.button("Delete all embeddings", on_click=llm_helper.vector_store.delete_keys_pattern, args=("doc*",), type="secondary")

except Exception as e:
    st.error(traceback.format_exc())

# flake8: noqa
from langchain.prompts import PromptTemplate

template = """{summaries}
Rispondi alla domanda in maniera discorsiva e completa usando solo le informazioni presenti nel testo sopra. 
Dopo ogni frase indica la fonte che hai utilizzato nel formato ##FONTE:
Se non trovi la risposta dì soltanto che non hai trovato informazioni nella documentazione indicizzata.
Question: {question}
Answer:"""

PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])

EXAMPLE_PROMPT = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)



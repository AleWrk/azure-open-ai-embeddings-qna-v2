# flake8: noqa
from langchain.prompts import PromptTemplate

template = """{summaries}
Rispondi alla domanda in maniera discorsiva e completa usando solo le informazioni presenti nel testo sopra.
Al termine della risposta elenca le "Fonti utilizzate" con un elenco numerato.
Nella riposta, accanto ad ogni frase indica il numero della fonte utilizzata nel formato [n].
Per ogni fonte riporta solo il nome del file.
Se non trovi la risposta dì soltanto che non hai trovato informazioni nella documentazione indicizzata e non tornare le fonti utilizzate.
Question: {question}
Answer:"""

PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])

EXAMPLE_PROMPT = PromptTemplate(
    template="Content: {page_content}\nSource: {source}",
    input_variables=["page_content", "source"],
)



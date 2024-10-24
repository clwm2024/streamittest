import base64
from dotenv import load_dotenv
from langchain.llms.openai import OpenAI
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
import openai
import os
import streamlit as st
import tempfile

PROMPT_TEMPLATE = """
Beantworte die Frage im folgenden Kontext:

{context}

---

Beantworte die Frage anhand des obenstehenden Kontexts: {question}
"""

# .env-Datei laden
try:
    load_dotenv('settings.env')
except:
    print("settings.env konnte nicht geladen werden.")
# Streamlit app
st.title('Test mit Langchain als Gitbot')

# OpenAI API Key laden
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key
print(openai_api_key)
if not openai_api_key is None:
    st.write(f'API Key vorhanden.')
else:
    st.write(f'API Key NICHT vorhanden.')

# Get OpenAI API key and source document input
#openai_api_key = st.text_input("OpenAI API Key", type="password")
try:
    # Lade die PDF-Datei als Byte-Stream
    pdf_path = "docs/HERMES2022_.pdf"
    # Lade die PDF-Datei als Byte-Stream
    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    # Konvertiere die PDF in Base64, um sie im iframe anzuzeigen
    source_doc = base64.b64encode(pdf_bytes).decode('utf-8')

except:
    source_doc = st.file_uploader("Upload Source Document", type="pdf")

# Check if the 'Summarize' button is clicked
if st.button("Summarize"):
    # Validate inputs
    if not openai_api_key.strip() or not source_doc:
        st.write(f"Bitte Datei hochladen")
    else:
        try:
            # Save uploaded file temporarily to disk, load and split the file into pages, delete temp file
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(source_doc.read())
            loader = PyPDFLoader(tmp_file.name)
            pages = loader.load_and_split()
            os.remove(tmp_file.name)
            
            # Create embeddings for the pages and insert into Chroma database
            embeddings=OpenAIEmbeddings(openai_api_key=openai_api_key)
            vectordb = Chroma.from_documents(pages, embeddings)

            # Initialize the OpenAI module, load and run the summarize chain
            llm=OpenAI(temperature=0, openai_api_key=openai_api_key)
            chain = load_summarize_chain(llm, chain_type="stuff")
            search = vectordb.similarity_search(" ")
            summary = chain.run(input_documents=search, question="Write a summary within 150 words.")
            
            st.write(summary)
        except Exception as e:
            st.write(f"An error occurred: {e}")

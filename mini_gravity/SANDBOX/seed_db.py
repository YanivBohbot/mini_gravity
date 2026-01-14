import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()
with open('politique_retour.txt', 'r', encoding='utf-8') as f: text = f.read()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.create_documents([text])
print('Vectorisation...')
db = Chroma.from_documents(docs, OpenAIEmbeddings(), persist_directory='./sandbox/chroma_db')
print('Succès ! Base remplie.')
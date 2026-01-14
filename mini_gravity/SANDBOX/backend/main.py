# import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

load_dotenv()

app = FastAPI()

# 1. Init Vector Store (La Mémoire)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = Chroma(
    persist_directory="./sandbox/chroma_db", embedding_function=embeddings
)

# 2. Init LLM (Le Cerveau)
llm = ChatOpenAI(model="gpt-4o", temperature=0)


class Question(BaseModel):
    question: str


@app.post("/chat")
async def chat_endpoint(body: Question):
    # Recherche dans la mémoire
    results = vector_store.similarity_search(body.question, k=3)

    # Préparation du contexte pour le cerveau
    context_str = "\n\n".join([doc.page_content for doc in results])

    # Instruction au cerveau
    template = """Tu es un expert du support client. Utilise le contexte suivant pour répondre.
    Contexte: {context}
    Question: {question}"""

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm

    # Génération de la réponse
    response = chain.invoke({"context": context_str, "question": body.question})

    return {"response": response.content}

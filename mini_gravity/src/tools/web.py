import os
from dotenv import load_dotenv  # <--- IMPORT IMPORTANT

# CHARGER LES VARIABLES D'ABORD

from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()
# On récupère notre base de données existante (la même que pour les PDF)
DB_DIRECTORY = "./sandbox/chroma_db"
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = Chroma(
    collection_name="agent_knowledge",
    embedding_function=embeddings,
    persist_directory=DB_DIRECTORY,
)


@tool
def search_web(query: str) -> str:
    """
    Cherche sur google  des informations technique a jour.
    utilise cette outil pour trouver des exemples des codes recents  ou des documentaiton
    retourne une liste durl et des resumes
    """

    try:
        search_tool = TavilySearch(max_results=3)
        results = search_tool.invoke(query)

        output = "Resultas de reecherche web : \n"
        for res in results:
            output += f"{res['content']} (URL: {res['url']})\n"
        return output
    except Exception as e:
        return f"❌ Erreur de recherche : {str(e)}"


@tool
def scrape_and_learn(url: str) -> str:
    """
    Visite une URL de documentation officielle, lit tout le contenu technique,
    et le mémorise dans la base de connaissances (Vector Store).
    À utiliser APRES avoir trouvé une URL pertinente avec search_web.
    """
    try:
        # load page
        loader = WebBaseLoader(url)
        docs = loader.load()
        # split docs
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)
        #  Mémorisation (RAG)
        vector_store.add_documents(documents=splits)

        return f"✅ J'ai lu la page {url} et j'ai appris {len(splits)} nouveaux concepts techniques."

    except Exception as e:
        return f"❌ Erreur lors de la lecture de la page : {str(e)}"


WEB_TOOLS = [search_web, scrape_and_learn]

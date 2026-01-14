import os
from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
# from langchain_core.vectorstores import InMemoryVectorStore


WORKING_DIRECTORY = "./SANDBOX"
DB_DIRECTORY = "./sandbox/chroma_db"


embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


#  initialisation du vectorstore
vector_Store = Chroma(
    collection_name="agent_Knowledge",
    embedding_function=embeddings,
    persist_directory=DB_DIRECTORY,
)


def _get_safe_path(filepath: str) -> str:
    """fonction utilitaire pour securiser les paths"""
    full_path = os.path.join(WORKING_DIRECTORY, filepath)
    return full_path


@tool
def ingest_file(filename: str) -> str:
    """
    Lit un fichier (PDF ou TXT) du dossier sandbox et l'ajoute à la mémoire.
    Args:
        filename: Le nom du fichier (ex: 'doc.pdf') qui doit être dans le dossier sandbox.
    """

    safe_path = _get_safe_path(filename)

    if not os.path.exists(safe_path):
        return (
            f"❌ Erreur : Le fichier {filename} n'existe pas dans le dossier sandbox."
        )

    try:
        if filename.lower().endswith(".pdf"):
            loader = PyPDFLoader(safe_path)
        else:
            loader = TextLoader(safe_path, encoding="utf-8")

        docs = loader.load()
        if not docs:
            return "⚠️ Le fichier semble vide ou illisible."

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        splitsDocuments = text_splitter.split_documents(docs)

        # 4. Indexation dans Chroma
        vector_Store.add_documents(documents=splitsDocuments)

        return f"✅ Succès : J'ai mémorisé {len(splitsDocuments)} fragments du fichier {filename}."
    except Exception as e:
        return f"❌ Erreur critique lors de l'ingestion : {str(e)}"


@tool
def search_knowledge(query: str) -> str:
    """
    Recherche une information dans la mémoire vectorielle.
    Args:
        query: La question ou le sujet à rechercher (ex: 'Comment installer FastAPI ?')
    """
    try:
        # On récupère les 3 morceaux les plus pertinents
        results = vector_Store.similarity_search(query, k=3)
        if not results:
            return "🤷 Aucune information trouvée dans ma mémoire sur ce sujet."
        # on format pour le LLM
        context_str = ""
        for i, doc in enumerate(results):
            source = os.path.basename(doc.metadata.get("source", "inconnu"))
            page = doc.metadata.get("page", "?")
            context_str += f"\n -- Extrait {i + 1} (Source: {source}, Page: {page}) ---\n{doc.page_content}\n"
        return context_str

    except Exception as e:
        return f"❌ Erreur de recherche : {str(e)}"


KNOWLEDGE_TOOLS = [ingest_file, search_knowledge]

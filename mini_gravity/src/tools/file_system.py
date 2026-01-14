import os
from langchain.tools import tool

WORKING_DIRECTORY = "./SANDBOX"

if not os.path.exists(WORKING_DIRECTORY):
    os.makedirs(WORKING_DIRECTORY)


def _get_safe_path(filepath: str) -> str:
    """fonction utilitaire pour securiser les paths"""
    full_path = os.path.join(WORKING_DIRECTORY, filepath)
    return full_path


@tool
def list_file() -> str:
    """liste tout les fichier et dossier dans le repertoire actuel du projet"""
    try:
        files = os.listdir(WORKING_DIRECTORY)
        return f"Fichier dans le projet :{', '.join(files)}"
    except Exception as e:
        return f"Erreur lors ede la lecture du dossier: {str(e)}"


@tool
def read_file(filepath: str) -> str:
    "lit le contenue dun fichier specifique , argument : filepath( ex:'main.py')"
    try:
        safe_path = _get_safe_path(filepath)
        if not os.path.exists(safe_path):
            return f"Erreur: le fichier {filepath} nexiste pas "

        with open(safe_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Erreur lors de la electure de {filepath}: {str(e)}"


@tool
def write_file(filepath: str, content: str) -> str:
    "Ecrit du contenu dans un fichier ecrase le contenue existant. Arguments: filepath , contents"
    try:
        safe_path = _get_safe_path(filepath)
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)

        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Succes: le fichier {filepath} a ete ecrit"
    except Exception as e:
        return f"Erreur lors de lecriture de {filepath}: {str(e)}"


ALL_TOOLS = [list_file, write_file, read_file]

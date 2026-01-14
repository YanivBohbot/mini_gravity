import operator
from typing import Annotated, List, TypedDict, Union
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    # memoir conversationelle (historique)
    messages: Annotated[List[BaseMessage], operator.add]
    # Le contexte de travail actuel
    current_working_directory: str

    # Les fichiers connus/chargés en mémoire tampon (pour éviter de tout relire à chaque fois)
    # Clé = Chemin du fichier, Valeur = Contenu
    file_cache: dict[str, str]

    # Compteur de boucle pour éviter les boucles infinies (sécurité)
    loop_step: int

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from src.tools.file_system import ALL_TOOLS as FS_TOOLS
from src.tools.terminal import ALL_TOOLS as TERM_TOOLS
from langchain_core.messages import SystemMessage
from src.tools.web import WEB_TOOLS
from src.tools.knowledge import search_knowledge
from src.tools_mcp.connector import load_tools as load_postgres
from src.state import AgentState
import asyncio
from dotenv import load_dotenv


load_dotenv()


# 2. Chargement des outils MCP
print("🐘 Connexion à PostgreSQL via MCP...")
db_tools = load_postgres()

# Petit check pour voir si ça a marché
if db_tools:
    print(f"✅ Base de données connectée ! Outils : {[t.name for t in db_tools]}")
else:
    print("⚠️ Attention : Pas de connexion base de données (Vérifie ton mot de passe).")

# --- Liste Finale des Outils ---
# On combine tout : Fichiers + Terminal + Web + Base de Données
ALL_TOOLS = FS_TOOLS + TERM_TOOLS + [search_knowledge] + WEB_TOOLS + db_tools


# --- 1. Initialisation du modèle ---
# On utilise gpt-4o pour sa capacité de raisonnement
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools(ALL_TOOLS)


# --- 2. Définition des Nœuds ---
def agent_node(state: AgentState):
    """Le cerveau de l'agent : décide quoi faire."""
    messages = state["messages"]

    # Injection du System Prompt si c'est le début
    if len(messages) == 1:
        if len(messages) == 1:
            system_prompt = SystemMessage(
                content="""Tu es un Développeur Full-Stack Autonome.

            GESTION DES PROCESSUS (TRES IMPORTANT):
            1. Pour installer ou configurer : Utilise `run_shell_command`.
            2. Pour lancer un SERVEUR (React, NestJS, Python API) : Utilise `start_background_process`.
            - Ne lance JAMAIS un serveur avec run_shell_command sinon tu seras bloqué.
            - Donne un nom clair au process (ex: 'api_server').
            3. Après avoir lancé un serveur : Attends quelques secondes et vérifie les logs avec `get_process_logs`.
            4. À la fin de ton travail : N'oublie pas de `stop_process`.

            Ta méthode : Search -> Learn -> Code -> Start Server -> Check Logs -> Verify.
            """
            )
        messages = [system_prompt] + messages

    # Appel au LLM
    response = llm_with_tools.invoke(messages)

    # Retourne le nouveau message
    return {"messages": [response]}


# Nœud pré-construit pour exécuter les outils
tool_node = ToolNode(ALL_TOOLS)

# --- 3. Logique de Routing ---


def should_continue(state: AgentState):
    """Décide si on arrête ou si on appelle un outil."""
    messages = state["messages"]
    last_message = messages[-1]

    # Si le LLM demande un outil -> direction "tools"
    if last_message.tool_calls:
        return "tools"

    # Sinon -> fin
    return END


# --- 4. Construction du Graphe ---

workflow = StateGraph(AgentState)

# ÉTAPE CRUCIALE : Ajout des nœuds (C'est ce qui manquait probablement)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# Définition du point de départ
workflow.add_edge(START, "agent")

# Définition des embranchements
workflow.add_conditional_edges(
    "agent",  # On part de l'agent
    should_continue,  # On vérifie la condition
    {
        "tools": "tools",  # Si outil nécessaire -> vers nœud 'tools'
        END: END,  # Sinon -> fin
    },
)

# Boucle de retour : Après un outil, on revient TOUJOURS à l'agent
workflow.add_edge("tools", "agent")

# Compilation
app = workflow.compile()

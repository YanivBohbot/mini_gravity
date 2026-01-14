import shutil
import asyncio
import nest_asyncio
import traceback  # <--- NOUVEAU
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

nest_asyncio.apply()

# ⚠️ VÉRIFIE BIEN CETTE LIGNE ⚠️
# As-tu bien mis TON mot de passe à la place de 'password' ?
# As-tu bien créé la base 'minigravity' ?
DB_URL = "postgresql://postgres:Mollokapi1@localhost:5433/minigravity"


async def get_postgres_tools():
    print(f"DEBUG: Vérification de 'uv'...")
    uv_path = shutil.which("uv")
    if not uv_path:
        print("❌ 'uv' non trouvé.")
        return []

    print(
        f"DEBUG: Lancement du serveur MCP avec : {DB_URL.replace(':', '***').split('@')[1]}"
    )  # On cache le mdp

    server_params = StdioServerParameters(
        command=uv_path,
        args=["x", "mcp-server-postgres", DB_URL],
    )

    try:
        async with stdio_client(server_params) as (read, write):
            print("DEBUG: Client stdio ouvert. Initialisation session...")
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("DEBUG: Session initialisée. Chargement outils...")

                tools = await load_mcp_tools(session)
                print(f"DEBUG: {len(tools)} outils trouvés.")
                return tools

    except Exception as e:
        print("\n❌ ERREUR DÉTAILLÉE :")
        # Ceci va afficher la vraie raison (mot de passe, connexion refusée...)
        traceback.print_exc()
        return []


def load_tools():
    try:
        return asyncio.run(get_postgres_tools())
    except Exception as e:
        print(f"⚠️ Erreur Wrapper : {e}")
        return []

import sys
from langchain_core.messages import HumanMessage
from src.graph import app
from src.state import AgentState


def main():
    print("🚀 Mini-Gravity est prêt. (Tapez 'q' pour quitter)")
    print("--------------------------------------------------")

    while True:
        try:
            user_input = input("\n👤 Vous: ")
            if user_input.lower() in ["q", "quit", "exit"]:
                print("Arrêt du système.")
                break

            # On prépare l'input pour le graphe
            # Note: On n'a pas besoin de gérer l'historique ici,
            # le 'memory' de LangGraph (checkpointer) pourrait le faire,
            # ou on renvoie simplement la liste mise à jour.
            initial_state = {"messages": [HumanMessage(content=user_input)]}

            print("\n🤖 Agent en cours de réflexion...\n")

            # STREAMING : On regarde chaque étape du graphe
            # stream_mode="values" nous renvoie l'état complet à chaque mise à jour
            for event in app.stream(initial_state, stream_mode="values"):
                # On récupère le dernier message ajouté à l'état
                messages = event.get("messages")
                if not messages:
                    continue

                last_message = messages[-1]

                # Cas 1 : L'Agent a décidé d'agir (Tool Call)
                if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                    for tool_call in last_message.tool_calls:
                        print(f"🛠️  [Action] Appel de : {tool_call['name']}")
                        print(f"    Arguments : {tool_call['args']}")

                # Cas 2 : L'Agent nous répond (Message final ou pensée)
                # On vérifie que ce n'est pas un message vide (souvent le cas lors des tool_calls)
                elif last_message.content:
                    # On affiche le contenu (parfois l'agent explique ce qu'il vient de faire)
                    # On évite de réafficher la question de l'utilisateur
                    if last_message.type == "ai":
                        print(f"🧠 [Agent]: {last_message.content}")

        except KeyboardInterrupt:
            print("\nArrêt forcé.")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    main()

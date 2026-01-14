import subprocess
import os
import signal
import time
from typing import Dict
from langchain_core.tools import tool

# Configuration
WORKING_DIRECTORY = "./sandbox"
LOGS_DIRECTORY = "./sandbox/logs"

# Assurons-nous que les dossiers existent
os.makedirs(WORKING_DIRECTORY, exist_ok=True)
os.makedirs(LOGS_DIRECTORY, exist_ok=True)

# Mémoire globale pour stocker les processus actifs (PID -> Popen Object)
# Attention: Cette mémoire est reset si on relance le script python main.py
ACTIVE_PROCESSES: Dict[str, subprocess.Popen] = {}


@tool
def run_shell_command(command: str) -> str:
    """
    Exécute une commande COURTE (ls, cat, pip install, mkdir).
    ATTENTION : Ne PAS utiliser pour lancer des serveurs qui ne s'arrêtent pas (node start, uvicorn, etc).
    """
    try:
        # Sécurité basique
        if "rm -rf /" in command:
            return "Erreur : Commande interdite."

        result = subprocess.run(
            command,
            shell=True,
            cwd=WORKING_DIRECTORY,
            capture_output=True,
            text=True,
            timeout=30,  # Timeout de sécurité augmenté
        )

        output = result.stdout
        error = result.stderr

        if result.returncode != 0:
            return f"❌ Erreur (Code {result.returncode}):\n{error}\n{output}"

        return f"✅ Sortie :\n{output}" if output else "✅ Succès (aucune sortie)."

    except subprocess.TimeoutExpired:
        return "❌ Erreur : Timeout. Pour les commandes longues/serveurs, utilise 'start_background_process'."
    except Exception as e:
        return f"❌ Erreur système : {str(e)}"


@tool
def start_background_process(command: str, name: str) -> str:
    """
    Lance un processus en arrière-plan (ex: npm run start, uvicorn, python app.py).
    Args:
        command: La commande à lancer.
        name: Un nom court pour identifier ce processus (ex: 'api_server').
    """
    try:
        # On définit un fichier de log pour capturer la sortie
        log_file_path = os.path.join(LOGS_DIRECTORY, f"{name}.log")
        log_file = open(log_file_path, "w", encoding="utf-8")

        # On lance le processus sans attendre (Popen)
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=WORKING_DIRECTORY,
            stdout=log_file,
            stderr=subprocess.STDOUT,  # On redirige les erreurs dans le même fichier
        )

        # On stocke le processus en mémoire
        ACTIVE_PROCESSES[name] = process

        return f"✅ Processus '{name}' démarré (PID: {process.pid}). Les logs sont dans {name}.log. Utilise 'get_process_logs' pour vérifier s'il tourne."

    except Exception as e:
        return f"❌ Erreur au démarrage : {str(e)}"


@tool
def stop_process(name: str) -> str:
    """Arrête un processus en arrière-plan par son nom."""
    if name not in ACTIVE_PROCESSES:
        return f"⚠️ Aucun processus trouvé avec le nom '{name}'."

    try:
        process = ACTIVE_PROCESSES[name]
        # On tue le processus et ses enfants (sur Windows taskkill est plus fiable)
        if os.name == "nt":  # Windows
            subprocess.run(f"taskkill /F /T /PID {process.pid}", shell=True)
        else:  # Linux/Mac
            os.kill(process.pid, signal.SIGTERM)

        del ACTIVE_PROCESSES[name]
        return f"🛑 Processus '{name}' arrêté avec succès."
    except Exception as e:
        return f"❌ Erreur lors de l'arrêt : {str(e)}"


@tool
def get_process_logs(name: str) -> str:
    """Lit les dernières lignes du fichier de log d'un processus."""
    log_file_path = os.path.join(LOGS_DIRECTORY, f"{name}.log")

    if not os.path.exists(log_file_path):
        return f"⚠️ Aucun log trouvé pour '{name}'."

    try:
        with open(log_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # On retourne les 20 dernières lignes
            tail = "".join(lines[-20:])
            return f"📜 Logs récents de '{name}':\n{tail}"
    except Exception as e:
        return f"❌ Erreur lecture logs : {str(e)}"


# On exporte la nouvelle liste
ALL_TOOLS = [
    run_shell_command,
    start_background_process,
    stop_process,
    get_process_logs,
]

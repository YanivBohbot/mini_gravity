import requests

# URL de l'API
url = "http://localhost:8000/chat"

# Données à envoyer à l'API
payload = {
    "question": "Quel est le délai de retour ?"
}

# Effectuer une requête POST
response = requests.post(url, json=payload)

# Afficher le statut de la réponse et le contenu
print("Statut de la réponse:", response.status_code)
print("Contenu de la réponse:", response.json())
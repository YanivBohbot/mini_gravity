import requests

# URL de l'API
url = 'http://localhost:8000/'

# Effectuer une requête GET
response = requests.get(url)

# Afficher le statut de la réponse et le contenu
print(f'Status Code: {response.status_code}')
print(f'Response Content: {response.text}')
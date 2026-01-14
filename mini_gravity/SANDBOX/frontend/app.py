import streamlit as st
import requests

st.title('Chat avec l\'API')

question = st.text_input('Entrez votre question:')

if st.button('Envoyer'):
    response = requests.post('http://localhost:8000/chat', json={'question': question})
    if response.status_code == 200:
        st.write('Réponse:', response.json().get('response', 'Pas de réponse'))
    else:
        st.write('Erreur:', response.status_code)
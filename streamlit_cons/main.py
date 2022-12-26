# Streamlit-Google Sheet
## Modules
import streamlit as st 
from pandas import DataFrame
import os
import openai

from gspread_pandas import Spread,Client
from google.oauth2 import service_account

from datetime import datetime

# Disable certificate verification (Not necessary always)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#Connect to openAI
def openai_connect():
    credential_openai= st.secrets["openai_creds"]
    openai.api_key = credential_openai.openai_api_key
    


st.header('Streamlit: Banco de Señales')

st.title('Información de la señal')
# Introducir el enlace
st.write('Introduce the link')
link = st.text_input('Link')

# Introducir el resumen
st.write('Introduce el resumen')
summary = st.text_input('Summary')


# Mostrar la información
st.title('Mostrar la información')
show = st.sidebar.button('Mostrar información OpenAI')
if show:
    what = "Get very short abstract in spanish of this text: "+summary
    why = 'Answer very shortly in spanish why is important this text: '+summary
    resumen_openai_what = openai.Completion.create(model="text-davinci-003", prompt=what, temperature=0, max_tokens=100)
    resumen_openai_why = openai.Completion.create(model="text-davinci-003", prompt=why, temperature=0, max_tokens=100)

    st.write('¿Sobre qué trata el texto?')
    st.write(resumen_openai_what['choices'][0]['text'])
    st.write('¿Por qué es importante?')
    st.write(resumen_openai_why['choices'][0]['text'])
else:
    st.write('No se ha mostrado la información')

